Model Execution
===============

Model execution and computation classes.

Model Runners
-------------

.. doxygenclass:: vajra::BaseModelRunner
   :members:

Model execution interface.

.. doxygenclass:: vajra::LLMModelRunner
   :members:

LLM-specific model execution.

Model Abstractions
------------------

.. doxygenclass:: vajra::BaseModel
   :members:

Model abstraction interface.

.. doxygenclass:: vajra::AttentionWrapper
   :members:

Attention mechanism implementations.

Workers
-------

.. doxygenclass:: vajra::BaseWorker
   :members:

Worker communication interface.

.. doxygenclass:: vajra::BaseLLMWorker
   :members:

LLM worker implementations.

.. doxygenclass:: vajra::PipelineParallelLLMWorker
   :members:

Pipeline parallel execution worker. 