Gammalearn Library
##################

Gammalearn leverages `pytorch lightning <https://lightning.ai/docs/pytorch/stable/>`_ to implement the training and 
testing of several neural network architectures for the analysis of the Cherenkov Telescope Array Observatory (CTAO) 
images. 

Models
******

All implemented models aim to predict, for a Data Level 1 (DL1) event: 

* the Cherenkov shower initial particle type. This is the so-called gammaness: the probability that the particle was 
  a gamma ray 
* the energy of the initial gamma ray.
* the direction of the gamma ray, as an offset from the telescope pointing
* the impact point: the coordinate of the intersection between the particle shower axis and the ground

This is refered to the **multi-task** objective of the models. As a consequence, all models follow a general structure:

* a **backbone** neural network computes a embedding (latent space representation) of the input
* 4 separate fully connected neural networks (with a single layer) predict, from the embedding, one of the task 
  value. Those are refered to *targets-networks*

There are two general architectures of backbone models implemented in the library: 

* `residual Convolutional Neural Network <https://en.wikipedia.org/wiki/Residual_neural_network>`_ (CNN) augmented 
  with `attention <https://en.wikipedia.org/wiki/Attention_(machine_learning)>`_. 
* `transformers <https://en.wikipedia.org/wiki/Transformer_(deep_learning_architecture)>`_ models.


Multi-modality
--------------

All models take as input the integrated charge images, and pixels maximum time map (the time, for each pixel, at which 
the waveform recorded by the pixel reached its maximal value).

However, in order to improve the performances, some models use additional inputs. The Conditional Batch Norm model, for
instance, can take the estimated night sky background (NSB) level as additional input to improve the generalization of 
the model to NSB levels not used during training. This is refered to as **multi-modality** models.

Domain Adaptation
-----------------

One challenge with deep learning methods applied to the analysis of the 
`Imaging Atmospheric Cherenkov Telescope <https://en.wikipedia.org/wiki/IACT>`_ is the abscense of labelled particle 
shower datasets. The supervised training of the models can only be performed using simulated data, which can not
represent exactly the real data. Models trained on simulation typically perform less well when used to predict real 
data events, due to the difference between the simulated training data and the real cherenkov images.

In order to teach the models this difference and improve generalization, **adversarial** unsupervised training can be 
leveraged. A new task is added to the network training: to discriminate between real data, and simulated data (real 
data images are mixed into the training data). However, the gradients of the discriminator are reversed when updating 
the backbone model, therefore the backbone model learns embeddings of the input data that maximizes the confusion 
between simulated and real data. The model implementing this technique is called **DANN**:Domain Adaptation Neural 
Network

The data from the labeled training set are refered to as the *source* data, and the data of the un-labelled training 
set are refered to as the *target* data.


Programs
********

The library programs are

* :py:func:`gammalearn.programs.gammalearn.main`: train and/or test a model. 
  Available as a command line program: ``gammalearn --help``
* :py:func:`gammalearn.programs.gl_dl1_to_dl2.main`: Use a trained model to make predictions
  Available as a command line program: ``gl_dl1_to_dl2 --help``


Code Organisation
*****************

Both library programs implement the following logic:

* parse the configuration file
* instantiate the :py:class:`~gammalearn.data.base_data_module.BaseDataModule` specialized class specified in the 
  experiment.
* Check the consistency of the data files
* Instantiate the model defined in the experiment settings
* Call :py:meth:`lightning.Trainer.fit` or :py:meth:`lightning.Trainer.test`



Configuration
-------------

The configuration of an experiment (train and/or test or prediction with ``gl_dl1_to_dl2``) is done through the 
definition of ``experiment_settings.py`` files that define the model's architecture, training/testing data modules, 
and training hyper-parameters.

The configuration setting file is loaded as a python module and parsed in the
:py:class:`gammalearn.experiment_runner.Experiment` class.

See `the examples <https://gitlab.in2p3.fr/gammalearn/gammalearn/-/tree/master/gammalearn/configuration/examples>`_ to 
learn more about the experiment settings file.


Data
----

Gammalearn implements loading mechanics for CTAO DL1 data, as well as image loading from class image digits datasets.
Available :py:class:`~lightning.pytorch.core.LightningDataModule` classes are:

* :py:class:`~gammalearn.data.LST_data_module.GLearnDataModule` to load CTAO DL1 data (simulation or real data). 
  Internally it will use the LST dataset classes:

  * :py:class:`~gammalearn.data.LST_dataset.MemoryLSTDataset` load all available data into RAM at initialization
  * :py:class:`~gammalearn.data.LST_dataset.FileLSTDataset` load data when queried

* :py:class:`~gammalearn.data.LST_data_module.GLearnDomainAdaptationDataModule` similar to the 
  :py:class:`~~gammalearn.data.LST_data_module.GLearnDataModule` but can mix real data and simulation to perform 
  domain adaptation

* :py:class:`~gammalearn.data.digit.digit_data_module.VisionDataModule` or 
  :py:class:`~gammalearn.data.digit.digit_data_module.VisionDomainAdaptationDataModule` to load data from classic 
  image digits dataset : mnist, mnistm, usps, without or with domain adaptation, respectively.

The writing of the model results is implemented in the :py:mod:`~gammalearn.data.save_results` module. In 
particular, the writing of the DL2 files is implemented in :py:mod:`~gammalearn.data.save_results.write_dl2_files` 
as a :py:class:`lightning.pytorch.callbacks.Callback`.

Datasets are able to discard a subset of the total events by applying filters, implemented in the
:py:mod:`gammalearn.data.dataset_event_filters` module.

Datasets are able to apply image processing transforms to the loaded images before handling them the model. The 
available transforms are in the :py:mod:`gammalearn.data.image_processing` module. The logic to apply the transforms 
is implemented in the base dataset classes, such as :py:mod:`gammalearn.data.LST_dataset.BaseLSTDataset` ; however some
transforms (such as noise addition) require additional input to be applied (the noise level). Therefore the actual 
application of the transforms is applied in the :py:func:`gammalearn.data.LST_dataset._get_image_data` abstract method
which is actually implemented in the children classes.

The dataset classes are only able to handle a single DL1 file. The dataset are merged together via the use of 
:py:class:`~torch.utils.data.ConcatDataset` in :py:class:`~gammalearn.data.LST_data_module.GLearnDataModule`. The 
datasets are all instantiated when :py:meth:`~gammalearn.data.LST_data_module.GLearnDataModule.get_dataset` is called, 
which can take a long time if the datasets load all the data upon instantiation 
(:py:class:`~gammalearn.data.LST_dataset.MemoryLSTDataset`).

To quickly test that a code is runing while limiting the amount of data loaded, `files_max_number=1` can be used in 
the experiment setting file. This will limit the DataModule number of datasets to 1, therefore loading a single DL1 
file.


Networks
--------

The neural network architectures are implemented in the :py:mod:`gammalearn.nets` module. The available backbone models
are

* :py:class:`~gammalearn.nets.residual_net.ResNetAttention` and its domain adversarial version 
  :py:class:`~gammalearn.nets.residual_net.ConditionalGammaPhysNet`

* :py:class:`~gammalearn.nets.transformer.GammaPhysNetPrime` and its domain adversarial version 
  :py:class:`~gammalearn.nets.transformer.GammaPhysNetMegatron`

The following classes can be interesting to understand the internal implementation:

* :py:class:`~gammalearn.nets.base.BaseBlock` implements the initialization of layers, addition of activation and 
  normalization layers

* :py:class:`~gammalearn.nets.sequential.ExtraKWArgsInForwardSequential` implements an equivalent of 
  :py:class:`torch.nn.Sequential` that allows to pass extra arguments from one layer to the next. This is used to pass
  multi-modality data to the layers, for instance the noise level.

* :py:class:`~gammalearn.nets.domain_adaptation.BaseDomainAdaptationNet` implements the use of gradient reversal layer.
  This allows to reverse the gradient of the discriminator when training with domain adaptation, there allowing to 
  train the backbone and the discriminator model at the same time.
  
* :py:class:`~gammalearn.nets.conditional_batch_normalization.CBN` implements the conditional batch norm layer, that
  learns the normalization to apply to its input based on a so-called "conditional" additional variable.


Criterions
----------

:py:mod:`gammalearn.criterion.multitask` implements the application of different loss function to each tasks.

The energy, gamma ray direction and impact tasks are only learned when the event is indeed a groundtruth gamma ray. 
Their losses are therefore not contributing to the global loss when the training data is a hadron. The mechanism to 
exclude these task losses is implemented by :py:class:`gammalearn.criterion.multitask.DomainConditionalLoss`.

Loss balancing
^^^^^^^^^^^^^^

When training multi-task models, one challenge is to balance the contribution of each task to the global training 
objective, in order for the network to learn to perform all tasks well. :py:mod:`gammalearn.criterion.loss_balancing` 
implements several loss balancing algorithms:

* :py:mod:`gammalearn.criterion.loss_balancing.uncertainty_weighting` weighting each task with uncertainty

* :py:mod:`gammalearn.criterion.loss_balancing.manual_weighting` weighting each task with manual weights

* :py:mod:`gammalearn.criterion.loss_balancing.manual_weighting` weighting each task based on the norm of the gradient 
  of the model with respect to the task.

Some of these methods, such as grad norm, require to learn the loss weights, therefore a second optimizer is used to 
train this model separately.

It is possible to exclude some losses from the set of losses optimized by the loss balancing, using
:py:class:`gammalearn.criterion.multitask.OutOfBalancing`. 

It is also possible to apply a weight that depends on the "training time" (batch or epoch index since the start of the 
training), which allows to slowly "introduce" a task in the optimization process, as a mean to mitigate the "conflicts"
between the tasks (the tasks gradient are "conflicting" when the gradient of model with respect to each task are not 
aligned, and the losses try to stear the model in opposite directions). This is implemented in the 
:py:mod:`gammalearn.criterion.loss_balancing.loss_weight_scheduler` module.


Monitoring
----------

Several quantities, such as the loss values, the loss balancing weights, the gradients of the model at certain layers, 
etc. can be logged for monitoring purposes during the training/testing of a model. This implemented in the 
:py:mod:`gammalearn.gl_logging` module, typically using :py:class:`lightning.pytorch.callbacks.Callback`


Data Flow
---------

Gammalearn models can make use of different input data, in addition to the integrated charge image and pulse maximum 
times. Unfortunately, the mechanisms to load and receive additional inputs are scattered around the code base

* :py:meth:`gammalearn.data.LST_dataset.BaseLSTDataset_get_sample` loads the dl1 parameters in addition to images and 
  time maps and outputs a dictionary of objects.

* the batch dictionary is converted to :py:class:`torch.Tensor` by the collate function 
  :py:meth:`gammalearn.data.base_data_module.BaseDataModule.collate_fn`

* the models receive the batch in the :py:meth:`gammalearn.gammalearn_lightning_module.training_step` function, which
  calls the training step of the actual model in :py:mod:`gammalearn.training_steps`, which eventually calls 
  :py:func:`gammalearn.training_steps.run_model` that actually access the data in the batch, depending on the 
  experiment settings stored in the :py:meth:`gammalearn.gammalearn_lightning_module.LitGLearnModule`


Transformers models need to have access to the camera geometry to compute the positional embedding of the tokens. The
geometry is read from the datasets in the experiment runner, and added to the net parameters dict. Therefore, 
transformers can use it even if it was not added in the experiment setting file.
