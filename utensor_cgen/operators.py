# -*- coding:utf8 -*-
from .snippets import *  # pylint: disable=W0401,W0614
from utensor_cgen.utils import NamescopedKWArgsParser
from utensor_cgen.transformer.optimizer import RefCntOptimizer

class _Operator(object):
  def __init__(self):
    self.name = ""
    self._snippet = None

  @property
  def snippet(self):
    return self._snippet


class _AddOperator(_Operator):
  def __init__(self, op_info):
    _Operator.__init__(self)
    inputs = [tensor_info.name for tensor_info in op_info.input_tensors]
    output = op_info.output_tensors[0].name
    tf_dtype = op_info.input_tensors[0].dtype
    parser = NamescopedKWArgsParser(RefCntOptimizer.KWARGS_NAMESCOPE, op_info.op_attr)
    ref_count = parser.get('ref_counts', [0])[0]
    to_eval = parser.get('to_eval', False)
    self._snippet = AddOpSnippet(inputs, output, tf_dtype, ref_count, to_eval)


class _ArgMaxOperator(_Operator):
  def __init__(self, op_info):
    _Operator.__init__(self)
    inputs = [tname for tname, _, _ in op_info.input_tensors]
    output, out_dtype, _ = op_info.output_tensors[0]
    _, in_dtype, _ = op_info.input_tensors[0]
    parser = NamescopedKWArgsParser(RefCntOptimizer.KWARGS_NAMESCOPE, op_info.op_attr)
    ref_count = parser.get('ref_counts', [0])[0]
    to_eval = parser.get('to_eval', False)
    self._snippet = ArgMaxOpSnippet(inputs, output, in_dtype, out_dtype, ref_count, to_eval)


class _DequantizeOperator(_Operator):
  def __init__(self, op_info):
    _Operator.__init__(self)
    inputs = [tname for tname, _, _ in op_info.input_tensors]
    output, out_dtype, _ = op_info.output_tensors[0]
    parser = NamescopedKWArgsParser(RefCntOptimizer.KWARGS_NAMESCOPE, op_info.op_attr)
    ref_count = parser.get('ref_counts', [0])[0]
    to_eval = parser.get('to_eval', False)
    self._snippet = DequantizeOpSnippet(inputs, output, out_dtype, ref_count, to_eval)


class _MaxOperator(_Operator):
  def __init__(self, op_info):
    _Operator.__init__(self)
    inputs = [tname for tname, _, _ in op_info.input_tensors]
    output, out_dtype, out_shape = op_info.output_tensors[0]
    # FIXME: automatic alloc for uTensor fail
    if not out_shape:
      out_shape = [1]
    parser = NamescopedKWArgsParser(RefCntOptimizer.KWARGS_NAMESCOPE, op_info.op_attr)
    ref_count = parser.get('ref_counts', [0])[0]
    to_eval = parser.get('to_eval', False)
    self._snippet = MaxOpSnippet(inputs, output, out_dtype, out_shape, ref_count, to_eval)


class _QuantizedMaxPool(_Operator):
  def __init__(self, op_info):
    _Operator.__init__(self)
    inputs = [tname for tname, _, _ in op_info.input_tensors]
    outputs = [tname for tname, _, _ in op_info.output_tensors]
    _, dtype, _ = op_info.output_tensors[0]
    ksize = op_info.op_attr['ksize'].value.ints_value
    strides = op_info.op_attr['strides'].value.ints_value
    padding = op_info.op_attr['padding'].value.decode('utf8')
    parser = NamescopedKWArgsParser(RefCntOptimizer.KWARGS_NAMESCOPE, op_info.op_attr)
    ref_counts = parser.get('ref_counts', [])
    to_eval = parser.get('to_eval', False)
    self._snippet = QuantizedMaxPoolSnippet(inputs, outputs, dtype,
                                            ksize, strides, padding,
                                            ref_counts, to_eval)


class _MinOperator(_Operator):
  def __init__(self, op_info):
    _Operator.__init__(self)
    inputs = [tname for tname, _, _ in op_info.input_tensors]
    output, out_dtype, out_shape = op_info.output_tensors[0]
    # FIXME: automatic alloc for uTensor fail
    if not out_shape:
      out_shape = [1]
    parser = NamescopedKWArgsParser(RefCntOptimizer.KWARGS_NAMESCOPE, op_info.op_attr)
    ref_count = parser.get('ref_counts', [0])[0]
    to_eval = parser.get('to_eval', False)
    self._snippet = MinOpSnippet(inputs, output, out_dtype, out_shape, ref_count, to_eval)


class _QuantizeV2Operator(_Operator):
  def __init__(self, op_info):
    _Operator.__init__(self)
    inputs = [tname for tname, _, _ in op_info.input_tensors]
    outputs = [tname for tname, _, _ in op_info.output_tensors]
    _, out_dtype, _ = op_info.output_tensors[0]
    parser = NamescopedKWArgsParser(RefCntOptimizer.KWARGS_NAMESCOPE,
                          op_info.op_attr)
    ref_counts = parser.get('ref_counts', [])
    to_eval = parser.get('to_eval', False)
    self._snippet = QuantizeV2OpSnippet(inputs, outputs, out_dtype, ref_counts, to_eval)


class _QuantizedMatMulOperator(_Operator):
  def __init__(self, op_info):
    _Operator.__init__(self)
    inputs = [tname for tname, _, _ in op_info.input_tensors]
    outputs = [tname for tname, _, _ in op_info.output_tensors]
    _, x_dtype, _ = op_info.input_tensors[0]
    _, w_dtype, _ = op_info.input_tensors[1]
    _, out_dtype, _ = op_info.output_tensors[0]
    parser = NamescopedKWArgsParser(RefCntOptimizer.KWARGS_NAMESCOPE,
                          op_info.op_attr)
    ref_counts = parser.get('ref_counts', [])
    to_eval = parser.get('to_eval', False)
    self._snippet = QuantizedMatMulOpSnippet(inputs, outputs,
                                             x_dtype, w_dtype, out_dtype, 
                                             ref_counts, to_eval)

class _QuantizedAddOperator(_Operator):
  def __init__(self, op_info):
    _Operator.__init__(self)
    inputs = [tname for tname, _, _ in op_info.input_tensors]
    outputs = [tname for tname, _, _ in op_info.output_tensors]
    _, x_dtype, _ = op_info.input_tensors[0]
    _, w_dtype, _ = op_info.input_tensors[1]
    _, out_dtype, _ = op_info.output_tensors[0]
    parser = NamescopedKWArgsParser(RefCntOptimizer.KWARGS_NAMESCOPE,
                          op_info.op_attr)
    ref_counts = parser.get('ref_counts', [])
    to_eval = parser.get('to_eval', False)
    self._snippet = QuantizedAddOpSnippet(inputs, outputs, 
                                          x_dtype, w_dtype, out_dtype, 
                                          ref_counts, to_eval)

class _QuantizedReluOperator(_Operator):
  def __init__(self, op_info):
    _Operator.__init__(self)
    inputs = [tname for tname, _, _ in op_info.input_tensors]
    outputs = [tname for tname, _, _ in op_info.output_tensors]
    _, in_dtype, _ = op_info.input_tensors[0]
    _, qout_dtype, _ = op_info.output_tensors[0]  #NT: why separate this out?
    out_dtypes = [t[1] for t in op_info.output_tensors[1:]]
    parser = NamescopedKWArgsParser(RefCntOptimizer.KWARGS_NAMESCOPE,
                                    op_info.op_attr)
    ref_counts = parser.get('ref_counts', [])
    to_eval = parser.get('to_eval', False)
    self._snippet = QuantizedReluOpSnippet(inputs, outputs, in_dtype,
                                           out_dtypes, qout_dtype, 
                                           ref_counts, to_eval)


class _RequantizationRangeOperator(_Operator):
  def __init__(self, op_info):
    _Operator.__init__(self)
    inputs = [tname for tname, _, _ in op_info.input_tensors]
    outputs = [tname for tname, _, _ in op_info.output_tensors]
    _, out_dtype, _ = op_info.output_tensors[0]
    parser = NamescopedKWArgsParser(RefCntOptimizer.KWARGS_NAMESCOPE,
                                    op_info.op_attr)
    ref_counts = parser.get('ref_counts', [])
    to_eval = parser.get('to_eval', False)
    self._snippet = RequantizationRangeOpSnippet(inputs, outputs, out_dtype, 
                                                 ref_counts, to_eval)


class _RequantizeOperator(_Operator):
  def __init__(self, op_info):
    _Operator.__init__(self)
    inputs = [tname for tname, _, _ in op_info.input_tensors]
    outputs = [tname for tname, _, _ in op_info.output_tensors]
    _, qout_dtype, _ = op_info.output_tensors[0]
    _, range_dtype, _ = op_info.output_tensors[1]
    parser = NamescopedKWArgsParser(RefCntOptimizer.KWARGS_NAMESCOPE,
                          op_info.op_attr)
    ref_counts = parser.get('ref_counts', [])
    to_eval = parser.get('to_eval', False)
    self._snippet = RequantizeOpSnippet(inputs, outputs,
                                        qout_dtype, range_dtype,
                                        ref_counts, to_eval)


class _ReshapeOperator(_Operator):
  def __init__(self, op_info):
    _Operator.__init__(self)
    inputs = [tname for tname, _, _ in op_info.input_tensors]
    output, _, _ = op_info.output_tensors[0]
    parser = NamescopedKWArgsParser(RefCntOptimizer.KWARGS_NAMESCOPE,
                          op_info.op_attr)
    ref_count = parser.get('ref_counts', [0])[0]
    to_eval = parser.get('to_eval', False)
    self._snippet = ReshapeOpSnippet(inputs, output, ref_count, to_eval)


class _QuantizedReshapeOperator(_Operator):
  def __init__(self, op_info):
    _Operator.__init__(self)
    inputs = [t_info.name for t_info in op_info.input_tensors]
    outputs = [t_info.name for t_info in op_info.output_tensors]
    parser = NamescopedKWArgsParser(RefCntOptimizer.KWARGS_NAMESCOPE,
                          op_info.op_attr)
    ref_counts = parser.get('ref_counts', [])
    to_eval = parser.get('to_eval', False)
    self._snippet = QuantizedReshapeOpSnippet(inputs=inputs,
                                              outputs=outputs,
                                              ref_counts=ref_counts,
                                              to_eval=to_eval)


class _Conv2DOperator(_Operator):
  def __init__(self, op_info):
    _Operator.__init__(self)
    inputs = [tname for tname, _, _ in op_info.input_tensors]
    outputs = [tname for tname, _, _ in op_info.output_tensors]
    _, in_dtype, _ = op_info.input_tensors[0]
    _, filter_dtype, _ = op_info.input_tensors[1]
    out_dtypes = [out_dtype for _, out_dtype, _ in op_info.output_tensors]
    strides = op_info.op_attr["strides"].value.ints_value
    padding = op_info.op_attr["padding"].value.decode('utf8')
    parser = NamescopedKWArgsParser(RefCntOptimizer.KWARGS_NAMESCOPE,
                          op_info.op_attr)
    ref_counts = parser.get('ref_counts', [])
    to_eval = parser.get('to_eval', False)
    self._snippet = Conv2DOpSnippent(inputs, outputs, strides, padding,
                                     in_dtype=in_dtype, filter_dtype=filter_dtype, out_dtypes=out_dtypes,
                                     ref_counts=ref_counts, to_eval=to_eval)


class OperatorFactory():
  # Can easily do something smarter
  _operators = {"Add": _AddOperator,
                "ArgMax": _ArgMaxOperator,
                "Dequantize": _DequantizeOperator,
                "Max": _MaxOperator,
                "QuantizedMaxPool": _QuantizedMaxPool,
                "Min": _MinOperator,
                "QuantizeV2": _QuantizeV2Operator,
                "QuantizedMatMul": _QuantizedMatMulOperator,
                "QuantizedRelu": _QuantizedReluOperator,
                "QuantizedAdd": _QuantizedAddOperator,
                "RequantizationRange": _RequantizationRangeOperator,
                "Requantize": _RequantizeOperator,
                "Reshape": _ReshapeOperator,
                "QuantizedReshape": _QuantizedReshapeOperator,
                "QuantizedConv2D": _Conv2DOperator}

  def createOperatorSnippet(self, op_info):
    op_type = op_info.op_type
    if op_type not in self._operators:
      err_msg = "unsupported op type in uTensor: {}".format(op_type)
      raise ValueError(err_msg)

    op = self._operators[op_type](op_info)  # Create desired object
    return op.snippet  # Ops know how to create their snippets
