import torch

from gammalearn.criterion.loss_balancing.loss_weight_scheduler import BaseW

# Used to have functions returning the training steps so that we could use a training step function with
# a value coming from a kwargs
# but this is not required anymore


def run_model(module, batch, train=True):
    """
    Run the model for one batch of data.

    If we do domain adaptation:
    First the data is retrieved from the batch and seperated into "source" and "target" (the 2 class of the domain adaptation)
    then the model is run on both source and target, with the required kwargs for each

    TODO: the only difference in the forward params between the source and target is the pointing
    it should be possible to stack then together and pass then both in the network at the same time to speed up training

    If we don't do domain adaptation:
    retrieve a batch, the forward parameters, and run the model

    Parameters
    ----------
        module: (LightningModule) The current module.
        batch: (torch.tensor) The current batch of data.
        train: (bool) Whether the current step is a training or a test step.
    """
    # TODO: isn't this done automatically by lightning ?
    module.net.train() if train else module.net.eval()

    forward_params = {}
    inputs_target, labels_target, outputs_target, dl1_params_target = None, None, None, None
    pointing_source, pointing_target = None, None

    if train and module.experiment.context["train"] == "domain_adaptation":
        # Load data
        inputs_source = batch["image_source"]
        inputs_target = batch["image_target"]
        labels_source = batch["label_source"]
        labels_target = batch.get("label_target", None)
        dl1_params_source = batch.get("dl1_params_source", None)
        dl1_params_target = batch.get("dl1_params_target", None)
        transform_params_source = batch.get("transform_params_source", {})
        transform_params_target = batch.get("transform_params_target", {})

        if dl1_params_source is not None:
            # Include the spurce alt/az information into the network
            alt_tel = batch["dl1_params_source"]["alt_tel"]
            az_tel = batch["dl1_params_source"]["az_tel"]
            pointing_source = torch.stack((alt_tel, az_tel), dim=1).to(torch.float32)

            # Include the target alt/az information into the network
            alt_tel = batch["dl1_params_target"]["alt_tel"]
            az_tel = batch["dl1_params_target"]["az_tel"]
            pointing_target = torch.stack((alt_tel, az_tel), dim=1).to(torch.float32)
    else:
        # Load data
        inputs_source = batch["image"]
        labels_source = batch.get("label", None)
        dl1_params_source = batch.get("dl1_params", None)
        transform_params_source = batch.get("transform_params", {})
        transform_params_target = {}

        # TODO: the dl1_params_source is always available for LST data, so we can always get the
        # pointing and source. However this function is used also with digit data, where these are not available
        # Include the alt/az information into the network
        if dl1_params_source is not None:
            alt_tel = batch["dl1_params"]["alt_tel"]
            az_tel = batch["dl1_params"]["az_tel"]
            pointing_source = torch.stack((alt_tel, az_tel), dim=1).to(torch.float32)

    # Include loss weighting if relevant
    # Scaling the losses is equivalent to scaling the gradient, so this is called grad_weigt
    # but the goal is to scale the losses, allowing to introduce a loss later in the training by increasing its weight
    if train:
        for _, v in module.experiment.targets.items():
            if v.get("grad_weight", None) is not None:
                if isinstance(v["grad_weight"], BaseW):
                    forward_params["grad_weight"] = v["grad_weight"].get_weight(module.trainer)
                else:
                    forward_params["grad_weight"] = v["grad_weight"]

    forward_params["pointing"] = pointing_source
    forward_params["transform_params"] = transform_params_source

    outputs_source = module.net(inputs_source, **forward_params)

    if inputs_target is not None:
        forward_params["pointing"] = pointing_target
        forward_params["transform_params"] = transform_params_target
        outputs_target = module.net(inputs_target, **forward_params)

    output_dict = {
        "inputs_source": inputs_source,
        "inputs_target": inputs_target,
        "labels_source": labels_source,
        "labels_target": labels_target,
        "dl1_params_source": dl1_params_source,
        "dl1_params_target": dl1_params_target,
        "outputs_source": outputs_source,
        "outputs_target": outputs_target,
    }

    return output_dict


def get_training_step_mae(**kwargs):
    def training_step_mae(module, batch):
        """
        The training operations for one batch for vanilla mt learning
        Parameters
        ----------
        module: LightningModule
        batch

        Returns
        -------

        """
        images = batch["image"]

        if module.net.add_pointing:
            pointing = torch.stack((batch["dl1_params"]["alt_tel"], batch["dl1_params"]["az_tel"]), dim=1).to(
                torch.float32
            )
            loss = module.net(images, pointing)
        else:
            loss = module.net(images)

        if module.experiment.regularization is not None:
            loss += (
                module.experiment.regularization["function"](module.net) * module.experiment.regularization["weight"]
            )

        return None, None, {"autoencoder": loss.detach().item()}, loss

    return training_step_mae


def get_eval_step_mae(**kwargs):
    def validation_step_mae(module, batch):
        """
        The training operations for one batch for vanilla mt learning
        Parameters
        ----------
        module: LightningModule
        batch

        Returns
        -------

        """
        images = batch["image"]

        if module.net.add_pointing:
            pointing = torch.stack((batch["dl1_params"]["alt_tel"], batch["dl1_params"]["az_tel"]), dim=1).to(
                torch.float32
            )
            loss = module.net(images, pointing)
        else:
            loss = module.net(images)

        return None, None, {"autoencoder": loss.detach().item()}, loss

    return validation_step_mae


# TODO: it is probably possible to combine the train step mae, the test_step mae and the train/test step mt into a single one
# and use it in the lightning module


def get_training_step_mt(**kwargs):
    def training_step_mt(module, batch):
        """
        The training operations for one batch for vanilla mt learning



        Parameters
        ----------
        module: LightningModule
        batch

        Returns
        -------

        """
        data = run_model(module, batch)
        outputs = data["outputs_source"]
        labels = data["labels_source"]
        # dl1_params = data["dl1_params_source"]

        # Compute loss
        loss, loss_data = module.experiment.LossComputing.compute_loss(outputs, labels, module)
        loss = module.experiment.loss_balancing(loss, module)
        loss = sum(loss.values())
        loss = module.experiment.LossComputing.regularization(loss, module)

        return outputs, labels, loss_data, loss

    return training_step_mt


def get_training_step_dann(**kwargs):
    def training_step_dann(module, batch):
        """
        The training operations for one batch
        Parameters
        ----------
        module: LightningModule
        batch

        Returns
        -------

        """
        data = run_model(module, batch)
        output = data["outputs_source"]
        labels = data["labels_source"]
        # dl1_params = data["dl1_params_source"]

        # Add the target class into the labels if setting the domain mask is necessary (check constants.py for real data)
        if "class" in data["labels_source"]:
            labels["domain_mask"] = torch.cat([data["labels_source"]["class"], data["labels_target"]["class"]])

        # Add the target domain into the output and labels
        output["domain_class"] = torch.cat([output["domain_class"], data["outputs_target"]["domain_class"]])
        labels["domain_class"] = torch.cat([labels["domain_class"], data["labels_target"]["domain_class"]])

        # Compute loss
        loss, loss_data = module.experiment.LossComputing.compute_loss(output, labels, module)
        loss = module.experiment.loss_balancing(loss, module)
        loss = sum(loss.values())
        loss = module.experiment.LossComputing.regularization(loss, module)

        return output, labels, loss_data, loss

    return training_step_dann


def get_eval_step_dann(**kwargs):
    def eval_step_dann(module, batch):
        """
        The validating operations for one batch
        Parameters
        ----------
        module
        batch

        Returns
        -------

        """
        data = run_model(module, batch)
        output = data["outputs_source"]
        labels = data["labels_source"]
        # dl1_params = data["dl1_params_source"]

        # Add the target class into the labels if setting the domain mask is necessary (check constants.py for real data)
        if "class" in data["labels_source"]:
            labels["domain_mask"] = torch.cat([data["labels_source"]["class"], data["labels_target"]["class"]])

        # Add the target domain into the output and labels
        output["domain_class"] = torch.cat([output["domain_class"], data["outputs_target"]["domain_class"]])
        labels["domain_class"] = torch.cat([labels["domain_class"], data["labels_target"]["domain_class"]])

        # Compute loss
        loss, loss_data = module.experiment.LossComputing.compute_loss(output, labels, module)
        loss = module.experiment.loss_balancing(loss, module)
        loss = sum(loss.values())

        return output, labels, loss_data, loss

    return eval_step_dann


def get_eval_step_mt(**kwargs):
    def eval_step_mt(module, batch):
        """
        The validating operations for one batch
        Parameters
        ----------
        module
        batch

        Returns
        -------

        """
        data = run_model(module, batch)
        outputs = data["outputs_source"]
        labels = data["labels_source"]
        # dl1_params = data["dl1_params_source"]

        # Compute loss and quality measures
        loss, loss_data = module.experiment.LossComputing.compute_loss(outputs, labels, module)
        loss = module.experiment.loss_balancing(loss, module)
        loss = sum(loss.values())

        return outputs, labels, loss_data, loss

    return eval_step_mt


def get_test_step_mt(**kwargs):
    def test_step_mt(module, batch):
        """
        The test operations for one batch
        Parameters
        ----------
        module
        batch

        Returns
        -------

        """
        data = run_model(module, batch, train=False)
        outputs = data["outputs_source"]
        labels = data["labels_source"]
        dl1_params = batch.get("dl1_params", None)

        return outputs, labels, dl1_params

    return test_step_mt
