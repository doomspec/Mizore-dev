from openfermion.ops import FermionOperator,QubitOperator

def spin_operators(n_qubit,fermion_qubit_transformation,opt_type,spin_separate=True):

    n0=n_qubit//2
    fermi_opt=FermionOperator()

    if spin_separate:
        spin_up=[i for i in range(n0)]
        spin_down=[i+n0 for i in range(n0)]
    else:
        spin_up=[2*i for i in range(n0)]
        spin_down=[2*i+1 for i in range(n0)]
        
    if opt_type=="Z":
        for i in range(0,n0):
            fermi_opt+=FermionOperator([(spin_up[i],1),(spin_up[i],0)])
        for i in range(0,n0):
            fermi_opt-=FermionOperator([(spin_down[i],1),(spin_down[i],0)])
        fermi_opt*=0.5
    if opt_type=="+":
        for i in range(0,n0):
            fermi_opt+=FermionOperator([(spin_up[i],1),(spin_down[i],0)])
    if opt_type=="-":
        for i in range(0,n0):
            fermi_opt+=FermionOperator([(spin_down[i],1),(spin_up[i],0)])
    
    qubit_s=fermion_qubit_transformation(fermi_opt)

    return qubit_s

def spin2_operator(n_qubit,transformation):
    Sp=spin_operators(n_qubit,transformation,"+")
    Sm=spin_operators(n_qubit,transformation,"-")
    Sz=spin_operators(n_qubit,transformation,"Z")
    Sx=0.5*(Sp+Sm)
    Sy=-0.5j*(Sp-Sm)
    from openfermion.utils import commutator
    res=Sz*Sz+Sy*Sy+Sx*Sx
    res.compress()
    return res