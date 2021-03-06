import sys
sys.path.append("./_lib/")
sys.path.append("./../_lib/")
import utils
import os

# Error Class:
def test_error():
  """
    Test Error Class.
  """
  assert utils.Error.not_found == 1

# Class ReplaceHelper:
def test_replace_helper():
  """
    Test ReplaceHelper Class.
  """
  # Test for ReplaceHelper.replace
  string = "__TEST__[[]]"
  rh = utils.ReplaceHelper("__")
  string = rh.replace(string, "TEST", "NEW")
  assert string == "NEW"
  # Test for ReplaceHelper.replace_with_default_value
  string = "__TEST__[[NEW]]"
  string = rh.replace_with_default_value(string,"TEST")
  assert string == "NEW"
  string = "__TEST__"
  string = rh.replace_with_default_value(string,"TEST")
  print "-->" + string
  assert string == ""

# Class Output:
def test_output():
  """
    Test Output Class.
  """
  out=utils.Output(5)
  assert out.BAR == "====="
  assert out.bar == "-----"
  assert out.BaR == "-=-=-"

  out.assert_msg(True, error_type=utils.Error.not_found)
  out.assert_msg(True)
  assert True

  out.exception_msg(utils.Error.not_found, "filename")
  assert True

  dictionary=dict()
  dictionary["test"]="test"
  out.print_dictionary(dictionary)
  assert True
  
  out.title("Title")
  assert True

  out.section("Title")
  assert True
  
  out.close_section()
  assert True

  out.close_subsection()
  assert True

  out.var("name","val")
  assert True

# Class ProcessEntry
def test_process_entry():
  """
    Test ProcessEntry Class.
  """
  out = utils.Output(5)
  pe = utils.ProcessEntry(out, section="section")
  
  string="@PWD@"
  assert pe.process(string) == os.getcwd().strip()
  string="PATH"
  string=pe.process(string)
  assert True
  string="@SIMULATION@"
  assert pe.process(string) == "section"
  string="@ENV[HOME]@"
  assert pe.process(string) == os.environ['HOME']
  string="/home///tmp/"
  assert pe.process(string) == "/home/tmp"
  
  simulation = dict()
  simulation["test"]="@SIMULATION@"
  simulations=[simulation]
  pe.process_a_simulation(simulations)
  assert simulations[0]["test"] == "section"

# Class GetValFromConfParser
import ConfigParser
def test_get_val_from_conf_parser():
  """
    Test GetValFromConfParser Class.
  """
  out = utils.Output(5)
  config = ConfigParser.RawConfigParser()
  config.add_section('Section1')
  config.set('Section1', 'item', 'val')
  extractor = utils.GetValFromConfParser(out, config, "Section1")
  assert extractor.get("item") == "val"
  assert extractor.get("item", True) == "val"

# Class GetValFromDictionary
def test_get_val_from_dictionary():
  """
    Test GetValFromDictionary Class.
  """
  out = utils.Output(5)
  dictionary = dict()
  dictionary['item'] = "val"
  extractor = utils.GetValFromDictionary(out, dictionary)
  assert extractor.get("item") == "val"
  assert extractor.get("not") == ""
  assert extractor.get("item", True) == "val"

# Class EvalExpression:
def test_eval_expression():
  """
    Test EvalExpression Class.
  """
  string = "@EVAL@[i for i in range(4)]"
  ee = utils.EvalExpression(string)
  ee.grep_expression()
  assert ee.expression == "i for i in range(4)"
  assert ee() == "0 || 1 || 2 || 3"
  string = "@PWD@"
  ee = utils.EvalExpression(string)
  assert ee() == "@PWD@"

  string = "@EVAL@[]"
  ee = utils.EvalExpression(string)
  ee.grep_expression()
  assert ee.expression == ""
  assert not ee()
  