#!/usr/bin/env python
# coding: utf-8

# In[3]:


def scheduling_exams(filename):
        #!/usr/bin/env python
    # coding: utf-8

    #reading input files to make graph

    f1 = open(filename+".crs","r")
    keys = []
    for x in f1:
        keys.append(x.split(' ')[0])

    #print(keys)
    graph = dict.fromkeys(keys,None)
    #print(graph)


    f = open(filename+".stu", "r")
    for x in f:
        #print(x)
       # print(x.split(' ')[0:3])
        for j in range(0,len(x.split(' '))-1):
            if( graph[x.split(' ')[j]] ) == None:

                graph[x.split(' ')[j]] = (x.split(' ')[0:len(x.split(' '))-1])
            else:
                for k in range(0,len(x.split(' '))-1):
                    graph[x.split(' ')[j]].append(x.split(' ')[k])

    # removing duplicates by making set and then list again and calculating degree
    graph2 = {a:list(set(b)) for a, b in graph.items()} #deleting 
    length = {a:len(b) for a, b in graph2.items()}
    #print(graph2)
    #print(length)

    #Deleting same node as key
    for k, v in graph2.items():
        #print((v))
        for i in range(0, len(v)):
            if(k == v[i]):
                v.remove(v[i])
                break


    #print(graph2)

    #greedy coloring for random node
    def color_nodes(g):
      # Order nodes in descending degree
        nodes = list(g.keys())
        color_map = {}

        for node in nodes:
            available_colors = [True] * len(nodes)
            for neighbor in g[node]:
                if neighbor in color_map:
                    color = color_map[neighbor]
                    available_colors[color] = False
            for color, available in enumerate(available_colors):
                if available:
                    color_map[node] = color
                    break

        return color_map


    color1 = color_nodes(graph2)
    slot1 = sorted(list(color1.keys()), key=lambda x: color1[x], reverse=True)
    #print(slot1)
    #print(color1)
    print("Total number of slot for random node:")
    print(int(color1[slot1[0]])+1)

    #greedy coloring for highest degree node
    def color_nodes2(g):
      # Order nodes in descending degree
        nodes = sorted(list(g.keys()), key=lambda x: len(g[x]), reverse=True)
        color_map = {}

        for node in nodes:
            available_colors = [True] * len(nodes)
            for neighbor in g[node]:
                if neighbor in color_map:
                    color = color_map[neighbor]
                    available_colors[color] = False
            for color, available in enumerate(available_colors):
                if available:
                    color_map[node] = color
                    break

        return color_map


    color2 = color_nodes2(graph2) #largest degree
    #print(color2)
    slot2 = sorted(list(color2.keys()), key=lambda x: color2[x], reverse=True)
    #print(slot1)
    #print(color1)
    print("Total number of slot for highest degree node:")
    print(int(color2[slot2[0]])+1)

    #sorting according to saturation degree, then highest degree
    def sort_nodelist(nodelist):  


        nodelist.sort(key = lambda x:(x[1],x[2]), reverse = True) 

        return nodelist[0] 



    # dsatur algorithm for coloring
    def color_nodes3(g):
        nodelist = []

        colormap ={}
        nodes = list(g.keys())
        for node in range(0,len(nodes)):
            nodelist.append([nodes[node], 0, len(g[nodes[node]])])

        #print(nodelist)
        adjacent_color_map = dict.fromkeys(nodes,None)


        while (len(nodelist)!= 0):
            available_colors = []
            for i in range(0,len(nodes)):
                 available_colors.append(True) 

            selectednode = sort_nodelist(nodelist)
            #print(selectednode)

            for neigh in g[selectednode[0]]:
                if neigh in colormap:
                    color = colormap[neigh]
                    available_colors[color] = False

            for color, available in enumerate(available_colors):
                if available:
                    colormap[selectednode[0]] = color
                    nodelist.remove(selectednode)

                    for neigh in g[selectednode[0]]:
                        if adjacent_color_map[neigh]==None:
                            adjacent_color_map[neigh]= set([color])
                        elif adjacent_color_map[neigh]!=None:
                            adjacent_color_map[neigh].add(color)
                        for k in range(0, len(nodelist)):
                            if(nodelist[k][0] == neigh):
                                nodelist[k][1] = len(adjacent_color_map[neigh])

                    break



        return colormap


    color3 =color_nodes3(graph2)
    #print(color3)
    slot3 = sorted(list(color3.keys()), key=lambda x: color3[x], reverse=True)
    #print(slot1)
    #print(color1)
    print("Total number of slot for Dsatur algorithm:")
    print(int(color2[slot3[0]])+1)

    #calculating penalty for all
    def penalty(color):
        f = open(filename+".stu", "r")
        templ =[]
        sum = 0
        count = 0
        for courses in f:
            count = count+1
            for k,v in color.items():
                courses = courses.replace(k, str(v))
            #print(courses)
            templ = [int(courses.split(' ')[v]) for v in range(0, len(courses.split(' '))-1)]
            templ.sort()
            #print(templ)
            for i in range(0,len(templ)-1):
                for j in range(i+1,len(templ)):
                    if(templ[j] - templ[i]) > 5:
                        sum = sum + 0
                    elif (templ[j] - templ[i]) <= 5:
                        if (templ[j] - templ[i])==1:
                            sum = sum +16
                        if (templ[j] - templ[i])==2:
                            sum = sum +8
                        if (templ[j] - templ[i])==3:
                            sum = sum +4
                        if (templ[j] - templ[i])==4:
                            sum = sum +2
                        if (templ[j] - templ[i])==5:
                            sum = sum +1

        return float(float(sum)/count)

    #penalties without kempe chain
    penalty1 = penalty(color1)
    print("Penalty without kempe chain for random node selection: ")
    print(penalty1)


    penalty2 = penalty(color2)
    print("Penalty without kempe chain for node with highest degree selection: ")
    print(penalty2)


    penalty3 = penalty(color3)
    print("Penalty without kempe chain for dsatur degree selection: ")
    print(penalty3)

    #bfs
    def bfs(g, start,color,colori,colorj):

        explored = []
        queue = [start]


        while queue:

            node = queue.pop(0)
            if node not in explored:
                explored.append(node)
                neighbours = g[node]

                for neighbour in neighbours:
                    if color[neighbour]==colori or color[neighbour] == colorj:
                        queue.append(neighbour)
        return explored

    #kempe chain
    import random
    def kempechain(g,color):
            vertex, adjacents = random.choice(list(g.items()))
            if(len(adjacents)==0):
                return
            second = random.choice(adjacents)
            p=penalty(color)

            #print(vertex,adjacents,second)
            colori = color[vertex]
            colorj = color[second]
            #print(colori,colorj)
            bfsfound = bfs(g,vertex,color,colori,colorj)
            #print(bfsfound, len(bfsfound))
            bfsfound.remove(vertex)
            bfsfound.remove(second)
    #         bfsfoundcolor = []
            color[second] = colori
            color[vertex] = colorj
            if(len(bfsfound)>1):
                for i in range(0, len(bfsfound)):
                    if(color[bfsfound[i]] == colori):
                        color[bfsfound[i]] = colorj
                    elif(color[bfsfound[i]]==colorj):
                        color[bfsfound[i]] = colori

            q = penalty(color)

            if(q>=p):
                color[second] = colori
                color[vertex] = colorj
                if(len(bfsfound)>1):
                    for i in range(0, len(bfsfound)):
                        if(color[bfsfound[i]] == colori):
                            color[bfsfound[i]] = colorj
                        elif(color[bfsfound[i]]==colorj):
                            color[bfsfound[i]] = colori





    #running kempe chain
    for i in range(0,1500):
        kempechain(graph2,color3)
    for i in range(0,1500):
        kempechain(graph2,color2)
    for i in range(0,1500):
        kempechain(graph2,color1)

    # Calculating penalty after kempe chain

    penalty4 = penalty(color3)
    print("Penalty with kempe chain for dsatur degree selection: ")
    print(penalty4)

    penalty5 = penalty(color2)
    print("Penalty with kempe chain for highest degree selection: ")
    print(penalty5)

    penalty6 = penalty(color1)
    print("Penalty with kempe chain for random node selection: ")
    print(penalty6)


# In[8]:


def scheduling_exams2(filename):
        #!/usr/bin/env python
    # coding: utf-8

    #reading input files to make graph

    f1 = open(filename+".crs","r")
    keys = []
    for x in f1:
        keys.append(x.split(' ')[0])

    #print(keys)
    graph = dict.fromkeys(keys,None)
    #print(graph)


    f = open(filename+".stu", "r")
    for x in f:
        #print(x)
       # print(x.split(' ')[0:3])
        for j in range(0,len(x.split(' '))-1):
            if( graph[x.split(' ')[j]] ) == None:

                graph[x.split(' ')[j]] = (x.split(' ')[0:len(x.split(' '))-1])
            else:
                for k in range(0,len(x.split(' '))-1):
                    graph[x.split(' ')[j]].append(x.split(' ')[k])

    # removing duplicates by making set and then list again and calculating degree
    graph2 = {a:list(set(b)) for a, b in graph.items()} #deleting 
    length = {a:len(b) for a, b in graph2.items()}
    #print(graph2)
    #print(length)

    #Deleting same node as key
    for k, v in graph2.items():
        #print((v))
        for i in range(0, len(v)):
            if(k == v[i]):
                v.remove(v[i])
                break


    #print(graph2)

    #greedy coloring for random node
    def color_nodes(g):
      # Order nodes in descending degree
        nodes = list(g.keys())
        color_map = {}

        for node in nodes:
            available_colors = [True] * len(nodes)
            for neighbor in g[node]:
                if neighbor in color_map:
                    color = color_map[neighbor]
                    available_colors[color] = False
            for color, available in enumerate(available_colors):
                if available:
                    color_map[node] = color
                    break

        return color_map


    color1 = color_nodes(graph2)
    slot1 = sorted(list(color1.keys()), key=lambda x: color1[x], reverse=True)
    #print(slot1)
    #print(color1)
    print("Total number of slot for random node:")
    print(int(color1[slot1[0]])+1)

    #greedy coloring for highest degree node
    def color_nodes2(g):
      # Order nodes in descending degree
        nodes = sorted(list(g.keys()), key=lambda x: len(g[x]), reverse=True)
        color_map = {}

        for node in nodes:
            available_colors = [True] * len(nodes)
            for neighbor in g[node]:
                if neighbor in color_map:
                    color = color_map[neighbor]
                    available_colors[color] = False
            for color, available in enumerate(available_colors):
                if available:
                    color_map[node] = color
                    break

        return color_map


    color2 = color_nodes2(graph2) #largest degree
    #print(color2)
    slot2 = sorted(list(color2.keys()), key=lambda x: color2[x], reverse=True)
    #print(slot1)
    #print(color1)
    print("Total number of slot for highest degree node:")
    print(int(color2[slot2[0]])+1)

    #sorting according to saturation degree, then highest degree
    def sort_nodelist(nodelist):  


        nodelist.sort(key = lambda x:(x[1],x[2]), reverse = True) 

        return nodelist[0] 



    # dsatur algorithm for coloring
    def color_nodes3(g):
        nodelist = []

        colormap ={}
        nodes = list(g.keys())
        for node in range(0,len(nodes)):
            nodelist.append([nodes[node], 0, len(g[nodes[node]])])

        #print(nodelist)
        adjacent_color_map = dict.fromkeys(nodes,None)


        while (len(nodelist)!= 0):
            available_colors = []
            for i in range(0,len(nodes)):
                 available_colors.append(True) 

            selectednode = sort_nodelist(nodelist)
            #print(selectednode)

            for neigh in g[selectednode[0]]:
                if neigh in colormap:
                    color = colormap[neigh]
                    available_colors[color] = False

            for color, available in enumerate(available_colors):
                if available:
                    colormap[selectednode[0]] = color
                    nodelist.remove(selectednode)

                    for neigh in g[selectednode[0]]:
                        if adjacent_color_map[neigh]==None:
                            adjacent_color_map[neigh]= set([color])
                        elif adjacent_color_map[neigh]!=None:
                            adjacent_color_map[neigh].add(color)
                        for k in range(0, len(nodelist)):
                            if(nodelist[k][0] == neigh):
                                nodelist[k][1] = len(adjacent_color_map[neigh])

                    break



        return colormap


    color3 =color_nodes3(graph2)
    #print(color3)
    slot3 = sorted(list(color3.keys()), key=lambda x: color3[x], reverse=True)
    #print(slot1)
    #print(color1)
    print("Total number of slot for Dsatur algorithm:")
    print(int(color2[slot3[0]])+1)

    #calculating penalty for all
    def penalty(color):
        f = open(filename+".stu", "r")
        templ =[]
        sum = 0
        count = 0
        for courses in f:
            count = count+1
            for k,v in color.items():
                courses = courses.replace(k, str(v))
            #print(courses)
            templ = [int(courses.split(' ')[v]) for v in range(0, len(courses.split(' '))-1)]
            templ.sort()
            #print(templ)
            for i in range(0,len(templ)-1):
                for j in range(i+1,len(templ)):
                    if(templ[j] - templ[i]) > 5:
                        sum = sum + 0
                    elif (templ[j] - templ[i]) <= 5:
                        if (templ[j] - templ[i])==1:
                            sum = sum +16
                        if (templ[j] - templ[i])==2:
                            sum = sum +8
                        if (templ[j] - templ[i])==3:
                            sum = sum +4
                        if (templ[j] - templ[i])==4:
                            sum = sum +2
                        if (templ[j] - templ[i])==5:
                            sum = sum +1

        return float(float(sum)/count)

    #penalties without kempe chain
    penalty1 = penalty(color1)
    print("Penalty without kempe chain for random node selection: ")
    print(penalty1)


    penalty2 = penalty(color2)
    print("Penalty without kempe chain for node with highest degree selection: ")
    print(penalty2)


    penalty3 = penalty(color3)
    print("Penalty without kempe chain for dsatur degree selection: ")
    print(penalty3)

    #bfs
    def bfs(g, start,color,colori,colorj):

        explored = []
        queue = [start]


        while queue:

            node = queue.pop(0)
            if node not in explored:
                explored.append(node)
                neighbours = g[node]

                for neighbour in neighbours:
                    if color[neighbour]==colori or color[neighbour] == colorj:
                        queue.append(neighbour)
        return explored

    #kempe chain
    import random
    def kempechain(g,color):
            vertex, adjacents = random.choice(list(g.items()))
            if(len(adjacents)==0):
                return
            second = random.choice(adjacents)
            #p=penalty(color)

            #print(vertex,adjacents,second)
            colori = color[vertex]
            colorj = color[second]
            #print(colori,colorj)
            bfsfound = bfs(g,vertex,color,colori,colorj)
            #print(bfsfound, len(bfsfound))
            bfsfound.remove(vertex)
            bfsfound.remove(second)
    #         bfsfoundcolor = []
            color[second] = colori
            color[vertex] = colorj
            if(len(bfsfound)>1):
                for i in range(0, len(bfsfound)):
                    if(color[bfsfound[i]] == colori):
                        color[bfsfound[i]] = colorj
                    elif(color[bfsfound[i]]==colorj):
                        color[bfsfound[i]] = colori

#             q = penalty(color)

#             if(q>=p):
#                 color[second] = colori
#                 color[vertex] = colorj
#                 if(len(bfsfound)>1):
#                     for i in range(0, len(bfsfound)):
#                         if(color[bfsfound[i]] == colori):
#                             color[bfsfound[i]] = colorj
#                         elif(color[bfsfound[i]]==colorj):
#                             color[bfsfound[i]] = colori





    #running kempe chain
    for i in range(0,2000):
        kempechain(graph2,color3)
    for i in range(0,2000):
        kempechain(graph2,color2)
    for i in range(0,2000):
        kempechain(graph2,color1)

    # Calculating penalty after kempe chain

    penalty4 = penalty(color3)
    print("Penalty with kempe chain for dsatur degree selection: ")
    print(penalty4)

    penalty5 = penalty(color2)
    print("Penalty with kempe chain for highest degree selection: ")
    print(penalty5)

    penalty6 = penalty(color1)
    print("Penalty with kempe chain for random node selection: ")
    print(penalty6)


# In[2]:


scheduling_exams("yor-f-83")


# In[9]:


scheduling_exams2("kfu-s-93")


# In[10]:


scheduling_exams2("tre-s-92")


# In[11]:


scheduling_exams2("car-f-92")


# In[12]:


scheduling_exams2("car-s-91")


# In[ ]:




