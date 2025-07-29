Core Engine
===========

Main inference engine and sequence management classes.

InferenceEngine
---------------

Main coordinator that orchestrates request processing, scheduling, and output generation.

.. doxygenclass:: vajra::InferenceEngine
   :members:

Sequence Management
-------------------

Core data structure for managing generation sequences with state tracking and memory allocation. 

.. doxygenclass:: vajra::Sequence  
   :members: