# Generates snippets/abaqus.json.
# Bodies start after the '*' you type yourself: type "*", then e.g. "node",
# pick the snippet, and it expands on the same line.
import json, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

S = {}
def add(prefix, desc, *lines):
    S[prefix] = {"prefix": prefix, "description": desc, "body": list(lines)}

# Model structure
add("Heading", "*Heading", "Heading", "${1:Model description}")
add("Part", "*Part ... *End Part", "Part, name=${1:Part-1}", "$0", "*End Part")
add("Assembly", "*Assembly ... *End Assembly", "Assembly, name=${1:Assembly}", "$0", "*End Assembly")
add("Instance", "*Instance ... *End Instance", "Instance, name=${1:Part-1-1}, part=${2:Part-1}", "${3:0.}, ${4:0.}, ${5:0.}", "*End Instance")
add("Step", "*Step ... *End Step", "Step, name=${1:Step-1}, nlgeom=${2|NO,YES|}", "$0", "*End Step")
add("Include", "*Include", "Include, input=${1:file.inp}")
add("Parameter", "*Parameter", "Parameter", "${1:name} = ${2:value}")
add("Restart", "*Restart, write", "Restart, write, frequency=${1:0}")
add("Preprint", "*Preprint", "Preprint, echo=${1|NO,YES|}, model=${2|NO,YES|}, history=${3|NO,YES|}, contact=${4|NO,YES|}")

# Mesh
add("Node", "*Node", "Node, nset=${1:nset_name}", "${2:1}, ${3:0.}, ${4:0.}, ${5:0.}")
add("Element", "*Element", "Element, type=${1:C3D8R}, elset=${2:elset_name}", "${3:1}, ${4:nodes}")
add("Nset", "*Nset", "Nset, nset=${1:Set-1}", "${2:1, 2, 3}")
add("Nset generate", "*Nset, generate", "Nset, nset=${1:Set-1}, generate", "${2:1}, ${3:100}, ${4:1}")
add("Elset", "*Elset", "Elset, elset=${1:Set-1}", "${2:1, 2, 3}")
add("Elset generate", "*Elset, generate", "Elset, elset=${1:Set-1}, generate", "${2:1}, ${3:100}, ${4:1}")
add("Surface", "*Surface, element based", "Surface, type=ELEMENT, name=${1:Surf-1}", "${2:elset}, ${3|S1,S2,S3,S4,S5,S6,SPOS,SNEG|}")
add("Surface node", "*Surface, node based", "Surface, type=NODE, name=${1:Surf-1}", "${2:nset}, ${3:1.}")

# Materials
add("Material", "*Material with density and elasticity", "Material, name=${1:Steel}", "*Density", "${2:7.85e-09},", "*Elastic", "${3:210000.}, ${4:0.3}")
add("Elastic", "*Elastic", "Elastic, type=${1|ISOTROPIC,ENGINEERING CONSTANTS,LAMINA,ORTHOTROPIC,ANISOTROPIC|}", "${2:210000.}, ${3:0.3}")
add("Density", "*Density", "Density", "${1:7.85e-09},")
add("Plastic", "*Plastic, isotropic hardening", "Plastic, hardening=${1|ISOTROPIC,KINEMATIC,COMBINED,JOHNSON COOK|}", "${2:250.}, ${3:0.}", "${4:300.}, ${5:0.05}")
add("Expansion", "*Expansion", "Expansion, zero=${1:20.}", "${2:1.2e-05},")
add("Conductivity", "*Conductivity", "Conductivity", "${1:50.},")
add("Specific Heat", "*Specific Heat", "Specific Heat", "${1:4.6e+08},")
add("Hyperelastic", "*Hyperelastic", "Hyperelastic, ${1|NEO HOOKE,MOONEY-RIVLIN,OGDEN,YEOH,ARRUDA-BOYCE|}", "${2:C10}, ${3:D1}")
add("Damping", "*Damping", "Damping, alpha=${1:0.}, beta=${2:0.}")

# Sections
add("Solid Section", "*Solid Section", "Solid Section, elset=${1:Set-1}, material=${2:Steel}", "${3:,}")
add("Shell Section", "*Shell Section", "Shell Section, elset=${1:Set-1}, material=${2:Steel}", "${3:1.}, ${4:5}")
add("Beam Section", "*Beam Section", "Beam Section, elset=${1:Set-1}, material=${2:Steel}, section=${3|RECT,CIRC,PIPE,BOX,I,L|}", "${4:dimensions}", "${5:0.}, ${6:0.}, ${7:-1.}")
add("Beam General Section", "*Beam General Section", "Beam General Section, elset=${1:Set-1}, section=${2|GENERAL,MESHED,NONLINEAR GENERAL|}", "${3:A}, ${4:I11}, ${5:I12}, ${6:I22}, ${7:J}", "${8:0.}, ${9:0.}, ${10:-1.}", "${11:E}, ${12:G}")
add("Membrane Section", "*Membrane Section", "Membrane Section, elset=${1:Set-1}, material=${2:Steel}", "${3:1.}")

# Steps
add("Static", "*Step with *Static and output", "Step, name=${1:Step-1}, nlgeom=${2|NO,YES|}", "*Static", "${3:1.}, ${4:1.}, ${5:1e-05}, ${6:1.}", "$0", "*Output, field, variable=PRESELECT", "*Output, history, variable=PRESELECT", "*End Step")
add("Dynamic Implicit", "*Step with implicit *Dynamic", "Step, name=${1:Step-1}, nlgeom=YES, inc=${2:1000}", "*Dynamic, application=${3|QUASI-STATIC,MODERATE DISSIPATION,TRANSIENT FIDELITY|}", "${4:0.01}, ${5:1.}, ${6:1e-08}, ${7:1.}", "$0", "*Output, field, variable=PRESELECT", "*Output, history, variable=PRESELECT", "*End Step")
add("Dynamic Explicit", "*Step with *Dynamic, Explicit", "Step, name=${1:Step-1}, nlgeom=YES", "*Dynamic, Explicit", ", ${2:1.}", "*Bulk Viscosity", "0.06, 1.2", "$0", "*Output, field, variable=PRESELECT, number interval=${3:20}", "*Output, history, variable=PRESELECT", "*End Step")
add("Frequency", "*Step with *Frequency (Lanczos)", "Step, name=${1:Frequency}, perturbation", "*Frequency, eigensolver=Lanczos, normalization=${2|DISPLACEMENT,MASS|}", "${3:10}, , , , ,", "$0", "*Output, field, variable=PRESELECT", "*End Step")
add("Buckle", "*Step with *Buckle", "Step, name=${1:Buckle}, perturbation", "*Buckle", "${2:5}, , ${3:18}, ${4:30}", "$0", "*Output, field, variable=PRESELECT", "*End Step")
add("Heat Transfer", "*Step with *Heat Transfer", "Step, name=${1:Heat}", "*Heat Transfer, ${2|steady state,end=PERIOD|}", "${3:1.}, ${4:1.}, ${5:1e-05}, ${6:1.}", "$0", "*Output, field, variable=PRESELECT", "*End Step")
add("Coupled Temp-Displacement", "*Step with *Coupled Temperature-Displacement", "Step, name=${1:Step-1}, nlgeom=YES", "*Coupled Temperature-Displacement, deltmx=${2:10.}", "${3:0.1}, ${4:1.}, ${5:1e-05}, ${6:1.}", "$0", "*Output, field, variable=PRESELECT", "*End Step")

# Loads and boundary conditions
add("Boundary", "*Boundary", "Boundary", "${1:nset}, ${2:1}, ${3:3}, ${4:0.}")
add("Boundary fixed", "*Boundary, fixed shorthand", "Boundary", "${1:nset}, ${2|ENCASTRE,PINNED,XSYMM,YSYMM,ZSYMM,XASYMM,YASYMM,ZASYMM|}")
add("Cload", "*Cload", "Cload", "${1:nset}, ${2:2}, ${3:-1000.}")
add("Dload", "*Dload", "Dload", "${1:elset}, ${2:GRAV}, ${3:9810.}, ${4:0.}, ${5:0.}, ${6:-1.}")
add("Dsload", "*Dsload", "Dsload", "${1:Surf-1}, P, ${2:1.}")
add("Amplitude", "*Amplitude, tabular", "Amplitude, name=${1:Amp-1}", "${2:0.}, ${3:0.}, ${4:1.}, ${5:1.}")
add("Temperature", "*Temperature", "Temperature", "${1:nset}, ${2:20.}")
add("Initial Conditions temperature", "*Initial Conditions, type=TEMPERATURE", "Initial Conditions, type=TEMPERATURE", "${1:nset}, ${2:20.}")
add("Initial Conditions stress", "*Initial Conditions, type=STRESS", "Initial Conditions, type=STRESS", "${1:elset}, ${2:S11}, ${3:S22}, ${4:S33}, ${5:S12}, ${6:S13}, ${7:S23}")
add("Initial Conditions velocity", "*Initial Conditions, type=VELOCITY", "Initial Conditions, type=VELOCITY", "${1:nset}, ${2:1}, ${3:0.}")

# Contact
add("Contact", "General contact, all exterior", "Contact", "*Contact Inclusions, ALL EXTERIOR", "*Contact Property Assignment", " ,  , ${1:IntProp-1}")
add("Contact Pair", "*Contact Pair", "Contact Pair, interaction=${1:IntProp-1}, type=${2|SURFACE TO SURFACE,NODE TO SURFACE|}", "${3:slave_surf}, ${4:master_surf}")
add("Surface Interaction", "*Surface Interaction with friction", "Surface Interaction, name=${1:IntProp-1}", "1.,", "*Friction", "${2:0.2},", "*Surface Behavior, pressure-overclosure=${3|HARD,EXPONENTIAL,LINEAR|}")
add("Friction", "*Friction", "Friction", "${1:0.2},")
add("Tie", "*Tie", "Tie, name=${1:Tie-1}, adjust=${2|yes,no|}, position tolerance=${3:0.1}", "${4:slave_surf}, ${5:master_surf}")

# Constraints and connectors
add("Kinematic Coupling", "*Coupling + *Kinematic", "Coupling, constraint name=${1:Coupling-1}, ref node=${2:ref_nset}, surface=${3:Surf-1}", "*Kinematic")
add("Distributing Coupling", "*Coupling + *Distributing", "Coupling, constraint name=${1:Coupling-1}, ref node=${2:ref_nset}, surface=${3:Surf-1}", "*Distributing, weighting method=${4|UNIFORM,LINEAR,QUADRATIC,CUBIC|}")
add("MPC", "*MPC", "MPC", "${1|BEAM,TIE,PIN,LINK|}, ${2:nset_a}, ${3:nset_b}")
add("Equation", "*Equation", "Equation", "${1:2}", "${2:nset_a}, ${3:1}, ${4:1.}, ${5:nset_b}, ${6:1}, ${7:-1.}")
add("Rigid Body", "*Rigid Body", "Rigid Body, ref node=${1:ref_nset}, elset=${2:elset}")
add("Transform", "*Transform", "Transform, nset=${1:nset}, type=${2|R,C,S|}", "${3:1.}, ${4:0.}, ${5:0.}, ${6:0.}, ${7:1.}, ${8:0.}")
add("Orientation", "*Orientation", "Orientation, name=${1:Ori-1}, system=${2|RECTANGULAR,CYLINDRICAL,SPHERICAL|}", "${3:1.}, ${4:0.}, ${5:0.}, ${6:0.}, ${7:1.}, ${8:0.}", "${9:3}, ${10:0.}")
add("Connector Section", "*Connector Section", "Connector Section, elset=${1:Wire-1-Set}", "${2|Beam,Hinge,Join,Cartesian,Bushing,Axial|},")

# Output
add("Output Field", "*Output, field with node and element output", "Output, field, frequency=${1:1}", "*Node Output", "${2:U, RF}", "*Element Output, directions=YES", "${3:S, E, PEEQ}")
add("Output History", "*Output, history", "Output, history, frequency=${1:1}", "*Energy Output", "${2:ALLIE, ALLKE}")
add("Node Output", "*Node Output", "Node Output${1:, nset=nset}", "${2:U, RF}")
add("Element Output", "*Element Output", "Element Output, directions=YES${1:, elset=elset}", "${2:S, E, PEEQ}")
add("Node Print", "*Node Print (to .dat)", "Node Print, nset=${1:nset}", "${2:U, RF}")
add("El Print", "*El Print (to .dat)", "El Print, elset=${1:elset}", "${2:S, E}")

json.dump(S, open("snippets/abaqus.json", "w"), indent=2)
print(len(S), "snippets")
