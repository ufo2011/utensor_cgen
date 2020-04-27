from tensorflow.tools.graph_transforms import TransformGraph
from utensor_cgen.frontend.tensorflow import GraphDefParser

from .base import Transformer
from .pipeline import TransformerPipeline

__all__ = ['QuantizeTransformer']

@TransformerPipeline.register_transformer
class QuantizeTransformer(Transformer):
  METHOD_NAME = 'quantize'
  KWARGS_NAMESCOPE = '_quantize'
  APPLICABLE_LIBS = set(["tensorflow"])

  def transform(self, ugraph):
    if ugraph.lib_name != 'tensorflow':
      raise ValueError('only support tensorflow graph')
    graph_def = ugraph.graph_def
    quant_graph_def = TransformGraph(input_graph_def=graph_def,
                                     inputs=[],
                                     outputs=ugraph.output_nodes,
                                     transforms=["quantize_weights", "quantize_nodes"])
    return GraphDefParser(config={}).parse(
      quant_graph_def,
      output_nodes=ugraph.output_nodes
    )
