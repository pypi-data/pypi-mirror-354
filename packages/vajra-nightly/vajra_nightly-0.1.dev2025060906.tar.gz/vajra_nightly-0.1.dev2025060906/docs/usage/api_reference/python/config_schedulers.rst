Scheduler Configuration
======================

This page documents the scheduler configuration classes for different scheduling strategies.

Base Scheduler
--------------

.. automodule:: vajra.config.replica_scheduler_config
   :members: BaseReplicaSchedulerConfig
   :undoc-members:
   :show-inheritance:

Fixed Chunk Scheduler
---------------------

.. autoclass:: vajra.config.replica_scheduler_config.FixedChunkReplicaSchedulerConfig
   :members:
   :undoc-members:
   :show-inheritance:

Dynamic Chunk Scheduler
------------------------

.. autoclass:: vajra.config.replica_scheduler_config.DynamicChunkReplicaSchedulerConfig
   :members:
   :undoc-members:
   :show-inheritance:

Space Sharing Scheduler
-----------------------

.. autoclass:: vajra.config.replica_scheduler_config.SpaceSharingReplicaSchedulerConfig
   :members:
   :undoc-members:
   :show-inheritance:

Request Prioritization
----------------------

FCFS Prioritizer
~~~~~~~~~~~~~~~~

.. autoclass:: vajra.config.request_prioritizer_config.FcfsRequestPrioritizerConfig
   :members:
   :undoc-members:
   :show-inheritance:

EDF Prioritizer
~~~~~~~~~~~~~~~

.. autoclass:: vajra.config.request_prioritizer_config.EdfRequestPrioritizerConfig
   :members:
   :undoc-members:
   :show-inheritance:

LRS Prioritizer
~~~~~~~~~~~~~~~

.. autoclass:: vajra.config.request_prioritizer_config.LrsRequestPrioritizerConfig
   :members:
   :undoc-members:
   :show-inheritance: 