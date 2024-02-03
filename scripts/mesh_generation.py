import json
import gmsh
import itertools


def get_tags_list(group):
    return [tag[1] for tag in group]


def generate_mesh(input_path, plot_mesh) :
    with open(input_path) as f:
        input = json.load(f)
        
    mesh_path = input["meshProperties"]["meshPath"]
    xmin = input["meshProperties"]["xmin"]
    xmax = input["meshProperties"]["xmax"]
    ymin = input["meshProperties"]["ymin"]
    ymax = input["meshProperties"]["ymax"]
    zmin = input["meshProperties"]["zmin"]
    zmax = input["meshProperties"]["zmax"]
    
    frac_data = input["meshProperties"]["fractureGeometry"]
    nFrac = frac_data["nFractures"]
    frac_coord = [frac_data["fractures"]["fracture{}".format(i)]["coordinates"] for i in range(nFrac)]
    
    well_data = input["wellData"]
    nWell = well_data["nWells"]
    well_coord = []
    init_frac = []
    for i in range(nWell):
        data = well_data["wells"][f"well{i}"]
        nPorts = data["nPorts"]
        for ip in range(nPorts):
            pdata = data["ports"][f"port{ip}"]
            well_coord.append(pdata["coordinates"])
            if data["isInitialHF"]:
                init_frac.append(pdata["initialFracture"]["coordinates"])
    
    gmsh.initialize()
    gmsh.model.add("2d-slice")
    s0 = (2, gmsh.model.occ.addRectangle(xmin, ymin, zmin, xmax-xmin, ymax-ymin))
    pfracs = []
    lfracs = []
    for i in range(nFrac):
        fc = frac_coord[i]
        pf1 = gmsh.model.occ.addPoint(fc[0], fc[1], zmin)
        pf2 = gmsh.model.occ.addPoint(fc[2], fc[3], zmin)
        lf = (1, gmsh.model.occ.addLine(pf1, pf2))
        pfracs.append([(0, pf1), (0, pf2)])
        lfracs.append(lf)
        
    pwells = []
    for i in range(len(well_coord)):
        wc = well_coord[i]
        pw = (0, gmsh.model.occ.addPoint(wc[0], wc[1], zmin))
        pwells.append(pw)
    
    linitfracs = []
    for i in range(len(init_frac)):
        fc = init_frac[i]
        pf1 = gmsh.model.occ.addPoint(fc[0], fc[1], zmin)
        pf2 = gmsh.model.occ.addPoint(fc[2], fc[3], zmin)
        lf = (1, gmsh.model.occ.addLine(pf1, pf2))
        linitfracs.append(lf)
        
    result = gmsh.model.occ.fragment([s0], [*lfracs, *linitfracs, *pwells])
    gmsh.model.occ.removeAllDuplicates()
    gmsh.model.occ.synchronize()

    eps = 1e-2
    domain_surfaces = gmsh.model.occ.getEntities(dim=2)
    frac_lines = []
    frac_points = []
    for i in range(nFrac):
        fc = frac_coord[i]
        fxmin = min(fc[0], fc[2])
        fxmax = max(fc[0], fc[2])
        fymin = min(fc[1], fc[3])
        fymax = max(fc[1], fc[3])
        fl = gmsh.model.occ.getEntitiesInBoundingBox(
            fxmin - eps, fymin - eps, zmin - eps,
            fxmax + eps, fymax + eps, zmin + eps, dim=1
        )
        pf = gmsh.model.occ.getEntitiesInBoundingBox(
            fxmin - eps, fymin - eps, zmin - eps,
            fxmax + eps, fymax + eps, zmin + eps, dim=0
        )
        frac_lines.extend(fl)
        frac_points.extend(pf)
    
    init_frac_lines = []
    init_frac_points = []
    for i in range(len(init_frac)):
        fc = init_frac[i]
        fl = gmsh.model.occ.getEntitiesInBoundingBox(
            fc[0] - eps, fc[1] - eps, zmin - eps,
            fc[2] + eps, fc[3] + eps, zmin + eps, dim=1
        )
        pf = gmsh.model.occ.getEntitiesInBoundingBox(
            fc[0] - eps, fc[1] - eps, zmin - eps,
            fc[2] + eps, fc[3] + eps, zmin + eps, dim=0
        )
        init_frac_lines.extend(fl)
        init_frac_points.extend(pf)
    init_frac_lines = list(set(init_frac_lines) - set(frac_lines))
    init_frac_points = list(set(init_frac_points) - set(frac_points))
    gmsh.model.addPhysicalGroup(2, get_tags_list(domain_surfaces), 100)
    # # gmsh.model.mesh.embed(1, get_tags_list(init_frac_lines), 2, get_tags_list(domain_surfaces)[0])
    # gmsh.model.mesh.embed(1, get_tags_list(init_frac_lines) + get_tags_list(frac_lines), 2, get_tags_list(domain_surfaces)[0])
    # gmsh.model.mesh.embed(0, get_tags_list(init_frac_points) + get_tags_list(init_frac_points), 2, get_tags_list(domain_surfaces)[0])
    
    h_frac = input["gmshProperties"]["hFrac"]
    h_default = input["gmshProperties"]["hDefault"]
    h_prod = input["gmshProperties"]["hProd"]
    dmin_frac = input["gmshProperties"]["distMinFrac"]
    dmax_frac = input["gmshProperties"]["distMaxFrac"]
    dmin_prod = input["gmshProperties"]["distMinProd"]
    dmax_prod = input["gmshProperties"]["distMaxProd"]
    
    ################## Boundary layer #######################
    frac_layer = gmsh.model.mesh.field.add('BoundaryLayer')
    curves_list = get_tags_list(frac_lines) + get_tags_list(init_frac_lines)
    gmsh.model.mesh.field.setNumbers(frac_layer, 'CurvesList', curves_list)
    gmsh.model.mesh.field.setNumbers(frac_layer, 'PointsList', get_tags_list(frac_points) + get_tags_list(init_frac_points))
    gmsh.model.mesh.field.setNumber(frac_layer, 'Size', h_frac)
    # sizes_list = len(get_tags_list(frac_points))*[h_frac] + len(get_tags_list(init_frac_points))*[h_prod]
    sizes_list = [[p, h_frac] for p in get_tags_list(frac_points)] + [[p, h_prod] for p in get_tags_list(init_frac_points)]
    sizes_list = list(itertools.chain(*sizes_list))
    # # gmsh.model.mesh.field.setNumber(frac_layer, 'SizesList', sizes_list)
    # gmsh.model.mesh.field.setNumber(frac_layer, 'Ratio', 1)
    # gmsh.model.mesh.field.setNumber(frac_layer, 'Quads', 1)
    # gmsh.model.mesh.field.setNumber(frac_layer, 'Thickness', dmin_frac)
    # # gmsh.model.mesh.field.setNumber(frac_layer, 'IntersectMetrics', 1)
    # gmsh.model.mesh.field.setAsBoundaryLayer(frac_layer)
    
    gmsh.model.mesh.field.setNumber(frac_layer, 'Size', 0.5*h_frac)
    # gmsh.model.mesh.field.setNumber(frac_layer, 'SizesList', sizes_list)
    gmsh.model.mesh.field.setNumber(frac_layer, 'Ratio', 1.1)
    gmsh.model.mesh.field.setNumber(frac_layer, 'Quads', 1)
    gmsh.model.mesh.field.setNumber(frac_layer, 'Thickness', dmin_frac)
    # gmsh.model.mesh.field.setNumber(frac_layer, 'BetaLaw', 1)
    # gmsh.model.mesh.field.setNumber(frac_layer, 'Beta', 1.001)
    # gmsh.model.mesh.field.setNumber(frac_layer, 'NbLayers', 8)
    # gmsh.model.mesh.field.setNumber(frac_layer, 'IntersectMetrics', 1)
    gmsh.model.mesh.field.setAsBoundaryLayer(frac_layer)
    
    
    ################## Field size #######################
    frac_distance = gmsh.model.mesh.field.add("Distance")
    gmsh.model.mesh.field.setNumbers(frac_distance, "CurvesList", get_tags_list(frac_lines))
    gmsh.model.mesh.field.setNumber(frac_distance, "Sampling", 2000)
    frac_threshold = gmsh.model.mesh.field.add("Threshold")
    gmsh.model.mesh.field.setNumber(frac_threshold, "InField", frac_distance)
    gmsh.model.mesh.field.setNumber(frac_threshold, "SizeMin", h_frac)
    gmsh.model.mesh.field.setNumber(frac_threshold, "SizeMax", h_default)
    gmsh.model.mesh.field.setNumber(frac_threshold, "DistMin", dmin_frac)
    gmsh.model.mesh.field.setNumber(frac_threshold, "DistMax", dmax_frac)
    
    
    init_frac_distance = gmsh.model.mesh.field.add("Distance")
    gmsh.model.mesh.field.setNumbers(init_frac_distance, "CurvesList", get_tags_list(init_frac_lines))
    init_frac_threshold = gmsh.model.mesh.field.add("Threshold")
    gmsh.model.mesh.field.setNumber(init_frac_threshold, "InField", init_frac_distance)
    gmsh.model.mesh.field.setNumber(init_frac_threshold, "SizeMin", h_prod)
    gmsh.model.mesh.field.setNumber(init_frac_threshold, "SizeMax", h_default)
    gmsh.model.mesh.field.setNumber(init_frac_threshold, "DistMin", dmin_prod)
    gmsh.model.mesh.field.setNumber(init_frac_threshold, "DistMax", dmax_prod)
    
    final_min_field = gmsh.model.mesh.field.add("Min")
    gmsh.model.mesh.field.setNumbers(final_min_field, "FieldsList", [frac_threshold, init_frac_threshold])
    gmsh.model.mesh.field.setAsBackgroundMesh(final_min_field)
    
    
    ################## Mesh options #######################
    gmsh.option.setNumber("Mesh.MeshSizeExtendFromBoundary", 0)
    gmsh.option.setNumber("Mesh.MeshSizeFromPoints", 0)
    gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 0)
    gmsh.option.setNumber("Mesh.RecombineAll", 1)
    gmsh.option.setNumber("Mesh.SubdivisionAlgorithm", 1)
    gmsh.option.setNumber("Mesh.RecombinationAlgorithm", 0)
    gmsh.option.setNumber("Mesh.Algorithm", 8)
    # gmsh.option.setNumber("Mesh.Algorithm", 6)


    ov = gmsh.model.occ.extrude(domain_surfaces, 0, 0, zmax-zmin, [1], recombine=True)
    gmsh.model.occ.synchronize()
    domain_volumes = gmsh.model.occ.getEntities(3)
    gmsh.model.addPhysicalGroup(3, get_tags_list(domain_volumes), 1000)

    gmsh.model.setColor(gmsh.model.occ.getEntities(2), 160, 32, 240) 
    gmsh.model.mesh.generate(3)
    gmsh.write(mesh_path)
    # Launch the GUI to see the results:
    if plot_mesh: gmsh.fltk.run()
    gmsh.finalize()