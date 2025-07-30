
# from orthpylib import a4d


# local test run from root:   python3 -m test.testlib
# from src.orthpylib import a4d
from src.orthpylib.orth_tools import get_linearization_matrix

# print ( a4d(1, 2) )
# get_linearization_matrix("model a \nend a;")

A, B, C, D = get_linearization_matrix("model BouncingBall3 extends Modelica.Icons.Example;\n import Modelica;\n parameter Integer order=3 \"Number of order of filter\";\n parameter Modelica.Units.SI.Frequency f_cut=2 \"Cut-off frequency\";\n parameter Modelica.Blocks.Types.FilterType filterType=Modelica.Blocks.Types.FilterType.LowPass\n \"Type of filter (LowPass/HighPass)\";\n parameter Modelica.Blocks.Types.Init init=Modelica.Blocks.Types.Init.SteadyState\n \"Type of initialization (no init/steady state/initial state/initial output)\";\n parameter Boolean normalized=true \"= true, if amplitude at f_cut = -3db, otherwise unmodified filter\";\n \n Modelica.Blocks.Sources.Step step(startTime=0.1, offset=0.1)\n annotation (Placement(transformation(extent={{-60,40},{-40,60}})));\n Modelica.Blocks.Continuous.Filter CriticalDamping(\n analogFilter=Modelica.Blocks.Types.AnalogFilter.CriticalDamping,\n normalized=normalized,\n init=init,\n filterType=filterType,\n order=order,\n f_cut=f_cut,\n f_min=0.8*f_cut)\n annotation (Placement(transformation(extent={{-20,40},{0,60}})));\n Modelica.Blocks.Continuous.Filter Bessel(\n normalized=normalized,\n analogFilter=Modelica.Blocks.Types.AnalogFilter.Bessel,\n init=init,\n filterType=filterType,\n order=order,\n f_cut=f_cut,\n f_min=0.8*f_cut)\n annotation (Placement(transformation(extent={{-20,0},{0,20}})));\n Modelica.Blocks.Continuous.Filter Butterworth(\n normalized=normalized,\n analogFilter=Modelica.Blocks.Types.AnalogFilter.Butterworth,\n init=init,\n filterType=filterType,\n order=order,\n f_cut=f_cut,\n f_min=0.8*f_cut)\n annotation (Placement(transformation(extent={{-20,-40},{0,-20}})));\n Modelica.Blocks.Continuous.Filter ChebyshevI(\n normalized=normalized,\n analogFilter=Modelica.Blocks.Types.AnalogFilter.ChebyshevI,\n init=init,\n filterType=filterType,\n order=order,\n f_cut=f_cut,\n f_min=0.8*f_cut)\n annotation (Placement(transformation(extent={{-20,-80},{0,-60}})));\n \n equation\n connect(step.y, CriticalDamping.u) annotation (Line(\n points={{-39,50},{-22,50}}, color={0,0,127}));\n connect(step.y, Bessel.u) annotation (Line(\n points={{-39,50},{-32,50},{-32,10},{-22,10}}, color={0,0,127}));\n connect(Butterworth.u, step.y) annotation (Line(\n points={{-22,-30},{-32,-30},{-32,50},{-39,50}}, color={0,0,127}));\n connect(ChebyshevI.u, step.y) annotation (Line(\n points={{-22,-70},{-32,-70},{-32,50},{-39,50}}, color={0,0,127}));\n \n  end BouncingBall3;\n\n\n\n\n")

print ( "A is " ,  A )
print ( "B is " ,  B )
print ( "C is " ,  C )
print ( "D is " ,  D )

