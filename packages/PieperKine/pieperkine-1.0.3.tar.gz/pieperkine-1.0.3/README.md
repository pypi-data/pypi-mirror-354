`PieperKine` is an analytical inverse kinematics calculation library for a 6-DOF robotic arm. When solving for inverse kinematics,

Here's a typical application example:

```python
from PieperKine import Pieper6dofKineSovler
import numpy as np
from spatialmath import SE3

# Define Denavit-Hartenberg parameters for Standard (S) and Modified (M) conventions
d1_s = 125.0000/1000;       a1_s = 0;                alpha1_s = np.pi/2;      theta1_s = 0;
d2_s = 0;                   a2_s = 300.0000/1000;    alpha2_s = 0;            theta2_s = np.pi/2;
d3_s = 0;                   a3_s = 0;                alpha3_s = np.pi/2;      theta3_s = 0;
d4_s = 250.000/1000;        a4_s = 0;                alpha4_s = np.pi/2;      theta4_s = 0;
d5_s = 0;                   a5_s = 0;                alpha5_s = -np.pi/2;     theta5_s = np.pi/2;
d6_s = 120.0000/1000;       a6_s = 0;                alpha6_s = 0;            theta6_s = 0;

# Modified DH parameters for the same robot
d1_m = 125.0000/1000;       a1_m = 0.0000;          alpha1_m = 0;           theta1_m = 0;
d2_m = 0;		            a2_m = 0.0000;          alpha2_m = np.pi/2;     theta2_m = np.pi/2;
d3_m = 0.0000;              a3_m = 300.0000/1000;   alpha3_m = 0;           theta3_m = 0;
d4_m = 250.000/1000;        a4_m = 0.0000;          alpha4_m = np.pi/2;     theta4_m = 0;
d5_m = 0.0000;              a5_m = 0.0000;          alpha5_m = np.pi/2;     theta5_m = -np.pi/2;
d6_m = 120.0000/1000;       a6_m = 0.0000;          alpha6_m = np.pi/2;     theta6_m = -np.pi;

# Assemble DH parameters into numpy arrays for the solver
SdhParams = np.array([
    [a1_s,    alpha1_s,     d1_s,     theta1_s],
    [a2_s,    alpha2_s,     d2_s,     theta2_s],
    [a3_s,    alpha3_s,     d3_s,     theta3_s],
    [a4_s,    alpha4_s,     d4_s,     theta4_s],
    [a5_s,    alpha5_s,     d5_s,     theta5_s],
    [a6_s,    alpha6_s,     d6_s,     theta6_s]
])

MdhParams = np.array([
    [a1_m,    alpha1_m,     d1_m,     theta1_m],
    [a2_m,    alpha2_m,     d2_m,     theta2_m],
    [a3_m,    alpha3_m,     d3_m,     theta3_m],
    [a4_m,    alpha4_m,     d4_m,     theta4_m],
    [a5_m,    alpha5_m,     d5_m,     theta5_m],
    [a6_m,    alpha6_m,     d6_m,     theta6_m]
])

# Define joint angle limits (in radians)
limit_n_j1 = -175 * deg2rad    # Minimum limit for joint 1
limit_p_j1 = 175 * deg2rad     # Maximum limit for joint 1

limit_n_j2 = -110 * deg2rad    # Minimum limit for joint 2
limit_p_j2 = 110 * deg2rad     # Maximum limit for joint 2

limit_n_j3 = -60 * deg2rad     # Minimum limit for joint 3
limit_p_j3 = 240 * deg2rad     # Maximum limit for joint 3

limit_n_j4 = -360 * deg2rad    # Minimum limit for joint 4
limit_p_j4 = 360 * deg2rad     # Maximum limit for joint 4

limit_n_j5 = -180 * deg2rad    # Minimum limit for joint 5
limit_p_j5 = 100 * deg2rad     # Maximum limit for joint 5

limit_n_j6 = -360 * deg2rad    # Minimum limit for joint 6
limit_p_j6 = 360 * deg2rad     # Maximum limit for joint 6

# Aggregate joint limits into a list for all 6 joints
Jointlimits = [
    [limit_n_j1, limit_p_j1],  # Joint 1
    [limit_n_j2, limit_p_j2],  # Joint 2
    [limit_n_j3, limit_p_j3],  # Joint 3
    [limit_n_j4, limit_p_j4],  # Joint 4
    [limit_n_j5, limit_p_j5],  # Joint 5
    [limit_n_j6, limit_p_j6]   # Joint 6
]

# ---- Inverse Kinematics Verification ----

# Counter for successful IK solutions
valid_ik_count = 0

# Create an instance of the Pieper 6-DOF kinematics solver
Pkine6 = Pieper6dofKineSovler(MdhParams, SdhParams, Jointlimits)

total = len(random_joint_angles)  # Total number of test samples

for i, jt_input in enumerate(random_joint_angles):
    # Compute the forward kinematics for this joint input
    Tfk = Pkine6.forwardKine(jt_input)
    np.random.seed(0)  # Set random seed for reproducibility

    # Add small random noise to the input joint angles for reference
    jt_ref = jt_input + (np.random.rand(*jt_input.shape) - 0.5) * 0.2  

    # Calculate the inverse kinematics from the forward kinematics result
    jt_clc_py, geoik_valid = Pkine6.inversKine(Tfk, jt_input)

    # Check if the calculated joint values are close to the original input
    if np.allclose(jt_input, jt_clc_py, atol=1e-2):
        valid_ik_count += 1  # Count as a valid IK solution
    else:
        print("jt_input: ")
        print(jt_input*rad2deg)
        print("jt_clc_py: ")
        print(jt_clc_py*rad2deg)
        
    # Print progress
    percent = (i + 1) / total * 100
    print(f"\rProgress: {percent:.1f}% ({i+1}/{total})", end='')

# Calculate and print the success rate of the inverse kinematics
success_rate = valid_ik_count / total * 100
print(f"\nInverse kinematics success rate: {success_rate:.2f}%")
