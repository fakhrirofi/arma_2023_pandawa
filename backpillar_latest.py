import itasca as it
import pandas as pd

it.command("python-reset-state false")

# sort data based on cohesive (DESCENDING)
material_data = [
    # [name, cohesive, thickness],
    ['BF cement 12%', 520567.051, 0],
    ['BF cement 10%', 442481.993, 4],
    ['BF cement 8%', 338368.583, 18],
    ['BF cement 6%', 234255.173, 20],
    ['BF cement 4%', 130141.763, 14],
    ['BF cement 2%', 52056.705, 16],
]
latest_fos = 3 # just initial, make it more 1.25
last_test = False
popped = 0

result_dir = "D:/ARMA/Template/data/experiment.csv"
result = pd.read_csv(result_dir)

large_strain = False

# OPTIMIZING ALGORITHM
dynamic_accuracy = [0.5, 1] # can switch -1 or +1
accuracy = dynamic_accuracy[0] #0.5 # unit divider, example acc=2, so 1/(2) = 0.5m (used accuracy in first run)

increment_i = -1 # increment index, EDIT IF RESUME
decrement_i = 0 # decrement index. this is an index of material data
# the increment already add material_data[index] thickness, vice versa
material_temp = list()
test_temp = dict()

while material_data[decrement_i][2] == 0:
    material_data.pop(0)
    popped += 1

# Create New Model
while True:
    test_name = "_".join(str(i[2]) for i in material_data)
    if test_name not in test_temp:
        it.command(f"""
        model new
        model large-strain {'on' if (large_strain == True) else 'off'}
        """)
        for i in range(len(material_data)):
            name = material_data[i][0]
            thickness = material_data[i][2]
            if i == 0:
                y1 = 0
                y2 = material_data[0][2]
            else:
                y1 = sum(i[2] for i in material_data[:i])
                y2 = sum(i[2] for i in material_data[:i+1])
            it.command(f"""
            ; Create Geometry
            zone create2d quadrilateral ...
                point 0 (0,{y1}) point 1 (15,{y1}) ...
                point 2 (0,{y2}) point 3 (15,{y2}) ...
                size {round(15*accuracy) if accuracy>1 else 15} {round(thickness*accuracy if accuracy>1 else thickness)} group '{name}' slot "Construction"
            """)
            
        it.command(f"""
        zone create2d quadrilateral ...
            point 0 (15,0) point 1 (16,0) ...
            point 2 (15,72) point 3 (16,72) ...
            size {round(1*accuracy) if accuracy>1 else 1} {round(72*accuracy) if accuracy>1 else 72} group 'rock' slot "Construction"

        ; Mechanical model and properties
        zone cmodel assign mohr-coulomb

        zone property density 2700 young 70e9 poisson 0.27 ...
            cohesion 30E6 friction 47 tension 10E6 ...
            range group 'rock'
        """)
        for i in range(len(material_data)):
            name = material_data[i][0]
            cohesive = material_data[i][1]
            it.command(f"""  
            zone property density 1550 young 430e6 poisson 0.39 ... 
                cohesion {cohesive} friction 35 tension 0.1e6 ...
                range group '{name}'
            """)
        for i in range(len(material_data)):
            # Create Geometries
            name = material_data[i][0]
            it.command(f"""  
            ; Interfaces
            zone interface create by-face separate range group '{name}' group 'rock'
            zone interface node property stiffness-normal 1E9 stiffness-shear 1E9
            zone interface node property friction 0
            """)
        it.command(f"""
        ; Boundary conditions 
        zone gridpoint fix velocity-x 0 range position-x 16
        zone gridpoint fix velocity-x 0 range position-x 0
        zone gridpoint fix velocity-y 0 range position-y 0

        model gravity 9.81
        
        zone initialize-stresses ratio 0.4264235636

        ;The maximum unbalanced force will never exactly reach zero 
        ;for a numerical analysis. The model is considered to be in 
        ;equilibrium when the maximum unbalanced force is small 
        ;compared to the representative forces in the problem.
        ;If the unbalanced force approaches a constant non-zero value,
        ;this probably indicates that interface slip, or zone failure
        ;and plastic flow are occurring within the model 
        ;(i.e., unstable).

        model history mechanical unbalanced-maximum

        model solve elas

        model save 'initial-equillibrium'

        ; Set non-zero inteface friction
        zone interface node property friction 35
        model solve

        ; Reset the displacements and velocities to ellimiante any numerical-only values.
        zone gridpoint initialize displacement (0,0) 
        zone gridpoint initialize velocity (0,0)

        ; Define some Histories along the backfill to be exposed.
        ; The x-displacement history is used to evaluate whether the system
        ; is coming to equilibrium at each step.
        history interval 50
        zone history name 'y6'  displacement-x position (0,6)
        zone history name 'y12' displacement-x position (0,12)
        zone history name 'y18' displacement-x position (0,18)
        zone history name 'y24' displacement-x position (0,24)
        zone history name 'y30' displacement-x position (0,30)
        zone history name 'y36' displacement-x position (0,36)
        zone history name 'y42' displacement-x position (0,42)
        zone history name 'y48' displacement-x position (0,48)
        zone history name 'y54' displacement-x position (0,54)
        zone history name 'y60' displacement-x position (0,60)
        zone history name 'y66' displacement-x position (0,66)

        model save 'initial-state'
        """)

        temp_data = dict() 
        for data in material_data:
            temp_data[data[0]] = [data[2]] # 'name' : [thickness]
            
        for i in range(12):
            y0 = 6 * i
            y1 = 6 * (i + 1)
            if i == 0:
                it.command("model restore 'initial-state'")
            else:
                it.command(f"model restore 'Cut-{str(i).zfill(2)}'")
            it.command(f"""
            zone gridpoint free velocity-x range position-x 0 position-y {y0} {y1}
            model solve 
            """)
            if i == 11:
                it.command("model step 5000")
            # Calculate FoS
            if large_strain == False:
                it.command(f"model factor-of-safety filename 'bf-fos-{i+1}'")
                latest_fos = it.fos()
                temp_data[f'fos{i+1}'] = [latest_fos]
                
            for view in ['History xdisp', 'Displacement', 'State', 'GP']:
                plotname = "_".join(["0"]*popped) \
                            + ("_" if popped else "") \
                            + "_".join([str(k[2]) for k in material_data])
                plotname = f"experiment/{plotname}_Cut-{str(i+1).zfill(2)}_{view}.png"
                it.command(f"plot '{view}' export bitmap file '{plotname}' size 950 720")
            max_disp = max(([(x.disp_x()**2 + x.disp_y()**2)**(1/2), x.pos()] for x in it.gridpoint.list()), key=lambda x: x[0])
            temp_data[f'disp{i+1}'] = [max_disp[0]]
            temp_data[f'pos{i+1}'] = ["_".join(str(i) for i in max_disp[1])]
                
            it.command(f"model save 'Cut-{str(i+1).zfill(2)}'")
            if latest_fos < 1.25 :
                break

        temp_result = pd.DataFrame(temp_data)
        result = result.append(temp_result,ignore_index=True)
        result.to_csv(result_dir)
    else:
        latest_fos = test_temp[test_name]
    
    if last_test == True:
        break
        
    # OPTIMIZING ALGORITHM
    # dynamic accuracy switch to left until max
    if latest_fos < 1.25:
        if len(material_temp):
            if material_temp[-1][2] < 0:
                material_data.insert(0, material_temp.pop())
        material_data[decrement_i][2] += (1 / accuracy) # reversed to > 1.25
        material_data[increment_i][2] -= (1 / accuracy)
        acc_index = dynamic_accuracy.index(accuracy)
        if acc_index != (len(dynamic_accuracy) - 1):
            accuracy = dynamic_accuracy[acc_index + 1]
        else:
            increment_i -= 1
            accuracy = dynamic_accuracy[0]
    elif len(material_temp):
        material_temp.clear()
        
    if material_data[increment_i][0] == material_data[decrement_i][0]:
        break
    
    material_data[decrement_i][2] -= (1 / accuracy) # reduce thickness
    material_data[increment_i][2] += (1 / accuracy) # add thickness
    if material_data[decrement_i][2] <= 0: 
        if material_data[decrement_i][2] < 0: #negative
            material_temp.append(material_data.pop(0))
        else:
            material_data.pop(0)
        popped += 1
        if len(material_data) == 1:
            last_test = True
    
    test_temp[test_name] = latest_fos
    