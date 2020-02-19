#Boris Giba
#2020
#code is not optimised and not commented yet


from tkinter import *
from time import sleep
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

#--------------------Model--------------------

class Node(Label):
    
    value_limits=[25,50,85] # moderate,medium,high
    
    def __init__(self,root,n_type,col,row,value_max=100):
        Label.__init__(self,root,width=3,height=1,borderwidth=1,relief="ridge",text=0,
                       bg="DarkSeaGreen1",fg="DarkSeaGreen1")
        self.type=n_type
        self.column=col
        self.row=row
        self.coords=[self.column,self.row]
        self.value=0
        self.emission_rate=0
        self.configure_type(self.type)
        self.level="low"
        self.value_limits=self.value_limits
        self.value_max=value_max
        
    @classmethod
    def get_wind_colour(self,value):
        #try:
        #    value_limits=self.value_limits
        #except:
        #    value_limits=[25,50,75]
        if value<self.value_limits[0]:
            colour="spring green"
        elif value<self.value_limits[1]:
            colour="deep sky blue"
        elif value<self.value_limits[2]:
            colour="chocolate3"
        else:
            colour="#B81365"

        return colour
    
    @classmethod
    def get_wind_colour2(self,value):
        colour=self.get_cell_colour(value)
        return colour

    @classmethod
    def get_cell_colour(self,value):
        #try:
        #    value_limits=self.value_limits
        #except:
        #    value_limits=[25,50,75]
        if value<self.value_limits[0]:
            colour="DarkSeaGreen1"
        elif value<self.value_limits[1]:
            colour="PaleTurquoise1"
        elif value<self.value_limits[2]:
            colour="burlywood1"
        else:
            colour="#D62626"#"#B81365"#ffcccb"
            
        return colour

    @classmethod
    def get_city_colour(self,n_type):
        if n_type=="village":
            colour="#1D7268"
        elif n_type=="small city":
            colour="#493438"
        else:
            colour="#AA46A4"

        return colour

    def configure_type(self,n_type):
        self.type=n_type
        if n_type=="basic":
            self.emission_rate=-1 #-5

        elif n_type=="village":
            self.emission_rate=(0,3) #15
            
        elif n_type=="small city":
            self.emission_rate=(1,5) #25
            
        elif n_type=="large city":
            self.emission_rate=(2,7) #35

    def iterate(self,show_numbers,current_iteration):
        if self.value>=0 and self.type!="basic" and self.value<self.value_max:
            self.value+=np.random.randint(self.emission_rate[0],self.emission_rate[1])
        else:
            if current_iteration%5==0 and self.value>0 and self.value<self.value_max:
                self.value+=self.emission_rate
        self.config(text=self.value)
        
        if self.value<self.value_limits[0]:
            #self.config(bg="DarkSeaGreen1",fg="black")#"DarkSeaGreen1")
            self.level="low"
            self.config(bg="DarkSeaGreen1",fg="black")
            if show_numbers==0:
                self.config(fg="DarkSeaGreen1")
            
        elif self.value<self.value_limits[1]:
            #self.config(bg="PaleTurquoise1",fg="black")#"PaleTurquoise1")
            self.level="moderate"
            self.config(bg="PaleTurquoise1",fg="black")
            if show_numbers==0:
                self.config(fg="PaleTurquoise1")
            
            
        elif self.value<self.value_limits[2]:
            #self.config(bg="burlywood1",fg="black")#"burlywood1")
            self.level="medium"
            self.config(bg="burlywood1",fg="black")
            if show_numbers==0:
                self.config(fg="burlywood1")
        else:
            #self.config(bg="#ffcccb",fg="black")#"#ffcccb")
            self.level="high"
            self.config(bg="#D62626",fg="white")
            if show_numbers==0:
                self.config(fg="#D62626")

class Calculator(object):
    def __init__(self):
        pass
    
    def revert_binary(self,b):
        if b==0:
            c=1
        else:
            c=0
        return c

    def get_neighbours(self,coords,n_type,maxima):
        #coords: (0,0)
        #maxima: 5
        if type(maxima)==int:
            maxima=[maxima,maxima]
        neighbours=[[],[]]
        if n_type=="large city":
            if coords[0]>0 and coords[1]>0 and coords[0]<maxima[0] and coords[1]<maxima[1]:
                neighbours[0].append( [ coords[0]+1, coords[1] ] )
                neighbours[0].append( [ coords[0], coords[1]+1 ] )
                neighbours[0].append( [ coords[0]-1, coords[1] ] )
                neighbours[0].append( [ coords[0], coords[1]-1 ] )
                neighbours[0].append( [ coords[0]+1, coords[1]+1 ] )
                neighbours[0].append( [ coords[0]-1, coords[1]-1 ] )
                neighbours[0].append( [ coords[0]+1, coords[1]-1 ] )
                neighbours[0].append( [ coords[0]-1, coords[1]+1 ] )

                neighbours[1].append(  [ coords[0]+2, coords[1] ] )
                neighbours[1].append(  [ coords[0]-2, coords[1] ] )
                neighbours[1].append(  [ coords[0], coords[1]+2 ] )
                neighbours[1].append(  [ coords[0], coords[1]-2 ] )

        if n_type=="small city" or n_type=="wind cell":
            if coords[0]>0 and coords[1]>0 and coords[0]<maxima[0]-1 and coords[1]<maxima[1]-1:
                neighbours[1].append( [ coords[0]+1, coords[1] ] )
                neighbours[1].append( [ coords[0], coords[1]+1 ] )
                neighbours[1].append( [ coords[0]-1, coords[1] ] )
                neighbours[1].append( [ coords[0], coords[1]-1 ] )

        if n_type=="city complex":
            if coords[0]>0 and coords[1]>0 and coords[0]<maxima[0]-1 and coords[1]<maxima[1]-1:
                neighbours[1].append( [ coords[0]+1, coords[1] ] )
                neighbours[1].append( [ coords[0], coords[1]+1 ] )
                neighbours[1].append( [ coords[0]-1, coords[1] ] )
                neighbours[1].append( [ coords[0], coords[1]-1 ] )

                neighbours[1].append( [ coords[0]+1, coords[1]+1 ] )
                neighbours[1].append( [ coords[0]-1, coords[1]-1 ] )
                neighbours[1].append( [ coords[0]+1, coords[1]-1 ] )
                neighbours[1].append( [ coords[0]-1, coords[1]+1 ] )

        return neighbours

    def calculate_wind_step(self,start_coords,left_chance,movement):
        #print("aaaaaa")
        next_coords=[]
        turn_chance=np.random.randint(0,101)

        turn=np.random.randint(0,101)
        next_coords=[ start_coords[0], start_coords[1] ]
        next_coords[ movement[0] ] += movement[1]
        if turn<turn_chance:
            direction=np.random.randint(0,101)
            if direction<left_chance:
                next_coords[ self.revert_binary(movement[0]) ] += movement[2]
            else:
                next_coords[ self.revert_binary(movement[0]) ] += movement[3]
                
        return next_coords

    def calculate_wind_path(self,start_coords,left_chance,maxima,movement,border_values):
        path=[start_coords]
        next_coords=self.calculate_wind_step(start_coords,left_chance,movement)
        if next_coords!=None:
            path.append(next_coords)
        #print(path[-1],border_values)
        while not ( (path[-1][0] in border_values[0]) or (path[-1][1] in border_values[1]) ):
            next_coords=self.calculate_wind_step(path[-1],left_chance,movement)
            path.append(next_coords)
        return path

    def expand_wind(self,path,expand_value,maxima,movement):
        #nochmal überarbeiten-> ordentlicher-> mit liste von paths statt einzeln!
        #expand: 1/2 (width 2 or width 3)
        direction=np.random.randint(0,2)
        path2=[]
        path3=[]
        for coords in path:
            expand=[coords[0],coords[1]]
            
            if expand_value==2:
                #print("dddaaaaammmnnn")
                expand2=[coords[0],coords[1]]
                expand[self.revert_binary(movement[0])]+=movement[1]
                expand2[self.revert_binary(movement[0])]-=movement[1]
                
                if expand[0]>0 and expand[1]>0 and expand[0]<maxima and expand[1]<maxima:
                    path2.append(expand)
                if expand2[0]>0 and expand2[1]>0 and expand2[0]<maxima and expand2[1]<maxima:
                    path3.append(expand2)
                
            elif direction==0:
                expand[self.revert_binary(movement[0])]+=movement[1]
            else:
                expand[self.revert_binary(movement[0])]-=movement[1]
            
            if expand[0]>0 and expand[1]>0 and expand[0]<maxima and expand[1]<maxima and expand_value==1:
                path2.append(expand)

        if expand_value==2:
            paths=[path2,path3]
            #print(paths,"t",path)
        else:
            paths=[path2]
            
        return paths

    def get_arrow(self,movement):
        arrow_list=[["←","→"],["↑","↓"]]
        if movement[1]==-1:
            movement[1]=0
        arrow=arrow_list[movement[0]][movement[1]]
        return arrow
        
class Wind(object):
    def __init__(self,path,amplitude,movement,width=1):
        self.amplitude=amplitude
        self.path=path
        self.width=width
        self.movement=movement

    def get_next_position(self):
        if len(self.path)!=0:
            next_pos=self.path[0]
            self.path.pop(0)
            return next_pos
        #else:
        #     next_pos=-1
        #return next_pos
    
#--------------------View--------------------

class Help(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.current_page=1
        self.page_commands=[self.page_1,self.page_2,self.page_3,
                            self.page_4,self.page_5,self.page_6,self.page_7]
        self.page_delete_commands=[self.delete_page_1,self.delete_page_2,self.delete_page_3,
                                   self.delete_page_4,self.delete_page_5,self.delete_page_6,self.delete_page_7]
        self.geometry("600x500")
        self.title("help / legend")
        self.config(bg="navy")
        self.next_page_button=Button(self,text="→",bg="light blue",activebackground="light blue",command=self.next_page,width=3)
        self.previous_page_button=Button(self,text="←",bg="light blue",activebackground="light blue",command=self.previous_page,width=3)
        self.page_text=Label(self,bg="navy",text="1 / 7",fg="white")
        self.next_page_button.place(x=340,y=440)
        self.previous_page_button.place(x=240,y=440)
        self.page_text.place(x=290,y=440)
        self.page_1()

    def next_page(self):
        self.page_delete_commands[self.current_page-1]()
        self.current_page+=1
        if self.current_page>7:
            self.current_page=1
        self.page_text.config(text=str(self.current_page)+" / 7")
        
        self.page_commands[self.current_page-1]()

    def previous_page(self):
        self.page_delete_commands[self.current_page-1]()
        self.current_page-=1
        if self.current_page<1:
            self.current_page=7
        self.page_text.config(text=str(self.current_page)+" / 7")

        self.page_commands[self.current_page-1]()

    def page_1(self):
        self.text1=Label(self,bg="navy",fg="white",justify="left",
                        text="""
                        Fine Dust - Wind Simulation,
                        or FiDuWiSi for short, is a small simulation program
                        designed to simulate the creation of fine dust,
                        or air pollution in general. To make this easier,
                        the process was extremely simplified. Certain areas
                        create fine dust in various amounts. Each iteration step
                        a wind may appear, which will take fine dust of the regions
                        it passes through with it. The winds have multiple attributes,
                        such as width or wind force.
                        """)
        self.text1.place(x=80,y=5)

    def page_2(self):
        self.text1=Label(self,bg="navy",fg="white",justify="left",
                        text="""
                        The map consists of cells.
                        On the left you can see one such cell.
                        Each cell represents f.e. one square kilometre.
                        When the grid is created,
                        some cells become villages,
                        small cities or even large cities.
                        On the left you can see an example of each.
                        You can see the different cells by pressing "view cities".
                        """)
        self.text2=Label(self,bg="navy",fg="white",justify="left",
                        text="""
                        However, because in reality it is pretty unlikely
                        to see a large city all by itself,
                        large cities are surrounded by small cities a few villages,
                        and small cities (which are not adjacent to a large city)
                        are surrounded by a few villages.
                        On the left you can see examples of each of the city groups.
                        """)

        self.text1.place(x=120,y=5)
        self.text2.place(x=120,y=150)
        field_colour=Node.get_cell_colour(0)
        village_colour=Node.get_city_colour("village")
        small_city_colour=Node.get_city_colour("small city")
        large_city_colour=Node.get_city_colour("large city")

        self.field=Label(self,text="",width=3,bg=field_colour,relief="ridge",height=1,borderwidth=1)
        self.village=Label(self,text="",width=3,bg=village_colour,relief="ridge",height=1,borderwidth=1)
        self.small_city=Label(self,text="",width=3,bg=small_city_colour,relief="ridge",height=1,borderwidth=1)
        self.large_city=Label(self,text="",width=3,bg=large_city_colour,relief="ridge",height=1,borderwidth=1)
        
        self.field_label=Label(self,text="field cell",bg="navy",fg="white")
        self.village_label=Label(self,text="village cell",bg="navy",fg="white")
        self.small_city_label=Label(self,text="small city cell",bg="navy",fg="white")
        self.large_city_label=Label(self,text="large city cell",bg="navy",fg="white")

        self.field.place(x=20,y=20)
        self.village.place(x=20,y=50)
        self.small_city.place(x=20,y=80)
        self.large_city.place(x=20,y=110)

        self.field_label.place(x=55,y=20)
        self.village_label.place(x=55,y=50)
        self.small_city_label.place(x=55,y=80)
        self.large_city_label.place(x=55,y=110)

        
        self.small_city1=Label(self,text="",width=3,bg=small_city_colour,relief="ridge",height=1,borderwidth=1)
        self.village1=Label(self,text="",width=3,bg=village_colour,relief="ridge",height=1,borderwidth=1)
        self.village2=Label(self,text="",width=3,bg=village_colour,relief="ridge",height=1,borderwidth=1)
        self.village3=Label(self,text="",width=3,bg=village_colour,relief="ridge",height=1,borderwidth=1)
        self.village4=Label(self,text="",width=3,bg=village_colour,relief="ridge",height=1,borderwidth=1)
        self.small_complex_label=Label(self,text="small city complex",bg="navy",fg="white")

        x_=70
        y_=200
        
        self.small_city1.place(x=x_,y=y_)
        self.village1.place(x=x_-25,y=y_)
        self.village2.place(x=x_+25,y=y_)
        self.village3.place(x=x_,y=y_+20)
        self.village4.place(x=x_,y=y_-20)
        self.small_complex_label.place(x=x_-38,y=y_+45)
        
        self.large_city1=Label(self,text="",width=3,bg=large_city_colour,relief="ridge",height=1,borderwidth=1)
        self.small_city2=Label(self,text="",width=3,bg=small_city_colour,relief="ridge",height=1,borderwidth=1)
        self.small_city3=Label(self,text="",width=3,bg=small_city_colour,relief="ridge",height=1,borderwidth=1)
        self.small_city4=Label(self,text="",width=3,bg=small_city_colour,relief="ridge",height=1,borderwidth=1)
        self.small_city5=Label(self,text="",width=3,bg=small_city_colour,relief="ridge",height=1,borderwidth=1)
        self.small_city6=Label(self,text="",width=3,bg=small_city_colour,relief="ridge",height=1,borderwidth=1)
        self.small_city7=Label(self,text="",width=3,bg=small_city_colour,relief="ridge",height=1,borderwidth=1)
        self.small_city8=Label(self,text="",width=3,bg=small_city_colour,relief="ridge",height=1,borderwidth=1)
        self.small_city9=Label(self,text="",width=3,bg=small_city_colour,relief="ridge",height=1,borderwidth=1)
        self.village5=Label(self,text="",width=3,bg=village_colour,relief="ridge",height=1,borderwidth=1)
        self.village6=Label(self,text="",width=3,bg=village_colour,relief="ridge",height=1,borderwidth=1)
        self.village7=Label(self,text="",width=3,bg=village_colour,relief="ridge",height=1,borderwidth=1)
        self.village8=Label(self,text="",width=3,bg=village_colour,relief="ridge",height=1,borderwidth=1)
        self.large_complex_label=Label(self,text="large city complex",bg="navy",fg="white")

        x_=70
        y_=340
        
        self.large_city1.place(x=x_,y=y_)
        self.small_city2.place(x=x_-25,y=y_)
        self.small_city3.place(x=x_+25,y=y_)
        self.small_city4.place(x=x_,y=y_+20)
        self.small_city5.place(x=x_,y=y_-20)
        self.small_city6.place(x=x_-25,y=y_-20)
        self.small_city7.place(x=x_-25,y=y_+20)
        self.small_city8.place(x=x_+25,y=y_-20)
        self.small_city9.place(x=x_+25,y=y_+20)
        self.village5.place(x=x_,y=y_+40)
        self.village6.place(x=x_,y=y_-40)
        self.village7.place(x=x_-50,y=y_)
        self.village8.place(x=x_+50,y=y_)
        self.large_complex_label.place(x=x_-36,y=y_+65)
    
    def page_3(self):
        self.text=Label(self,bg="navy",fg="white",justify="left",
                text="""
                Each cell has a certain concentration of fine dust,
                represented through
                an integer between 0 ( (close to) none) and 100 (highly polluted.
                You can view all of the concentration values by pressing "view numbers".
                Villages,as well as small and large cities
                generate a certain amount of fine dust every iteration step,
                which varies slightly. Large cities generate the most,
                followed by small cities and lastly villages.
                Field cells do not generate any dust, in fact,
                if a wind blows fine dust onto a field cell,
                it will start to slowly decrease. This shall simulate the
                dust falling down onto the fields.
                Cells with a medium or high amount of dust
                will scatter a small amount (2-3%)
                of their fine dust concenctration onto neighbouring cells
                each iteration, with a higher concentration leading to
                more fine dust being scattered, because it would not make
                a lot of sense if one cell would contain perfect air while
                a neighbouring cell always has completely polluted air.
                """)
        self.text.place(x=120,y=10)
        
        village_colour=Node.get_city_colour("village")
        small_city_colour=Node.get_city_colour("small city")
        
        self.village=Label(self,text="15",width=3,bg=village_colour,fg="white",relief="ridge",height=1,borderwidth=1)
        self.village.place(x=65,y=50)
        self.value_label=Label(self,text="each cell has a certain concentration of fine dust",bg="navy",fg="white",wraplength=150)
        self.value_label.place(x=5,y=75)

        self.small_city1=Label(self,text="-8",width=3,bg=small_city_colour,fg="white",relief="ridge",height=1,borderwidth=1)
        self.village1=Label(self,text="+2",width=3,bg=village_colour,fg="white",relief="ridge",height=1,borderwidth=1)
        self.village2=Label(self,text="+2",width=3,bg=village_colour,fg="white",relief="ridge",height=1,borderwidth=1)
        self.village3=Label(self,text="+2",width=3,bg=village_colour,fg="white",relief="ridge",height=1,borderwidth=1)
        self.village4=Label(self,text="+2",width=3,bg=village_colour,fg="white",relief="ridge",height=1,borderwidth=1)
        self.scatter_label=Label(self,text="high amounts of dust scatter onto neighbouring cells",bg="navy",fg="white",wraplength=150)

        x_=65
        y_=200
        
        self.small_city1.place(x=x_,y=y_)
        self.village1.place(x=x_-25,y=y_)
        self.village2.place(x=x_+25,y=y_)
        self.village3.place(x=x_,y=y_+20)
        self.village4.place(x=x_,y=y_-20)
        self.scatter_label.place(x=5,y=y_+45)

    def page_4(self):
        self.text=Label(self,bg="navy",fg="white",justify="left",
                text="""
                Each tile holds a certain colour which depends
                on the concentration of fine dust in said area.
                There are four different levels:
                low, moderate, medium and high.
                A cell of each level is visible on the left.
                """)
        self.text2=Label(self,bg="navy",fg="white",justify="left",
                text="""
                Winds share a similar, slightly more saturated
                colour-map to make them more easily visible.
                You can disable
                this highlighting in the "configure params"-menu.
                """)
        self.text.place(x=120,y=10)
        self.text2.place(x=120,y=200)
        low_colour=Node.get_cell_colour(10)
        moderate_colour=Node.get_cell_colour(30)
        medium_colour=Node.get_cell_colour(55)
        high_colour=Node.get_cell_colour(85)

        low_wind_colour=Node.get_wind_colour(10)
        moderate_wind_colour=Node.get_wind_colour(30)
        medium_wind_colour=Node.get_wind_colour(55)
        high_wind_colour=Node.get_wind_colour(85)
        
        #25,50,85
        
        self.low=Label(self,text="10",width=3,bg=low_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.moderate=Label(self,text="30",width=3,bg=moderate_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.medium=Label(self,text="55",width=3,bg=medium_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.high=Label(self,text="90",width=3,bg=high_colour,fg="white",relief="ridge",height=1,borderwidth=1)

        self.low_wind=Label(self,text="↑",width=3,bg=low_wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.moderate_wind=Label(self,text="↑",width=3,bg=moderate_wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.medium_wind=Label(self,text="↑",width=3,bg=medium_wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.high_wind=Label(self,text="↑",width=3,bg=high_wind_colour,fg="white",relief="ridge",height=1,borderwidth=1)

        self.low_label=Label(self,text="low",bg="navy",fg="white")
        self.moderate_label=Label(self,text="moderate",bg="navy",fg="white")
        self.medium_label=Label(self,text="medium",bg="navy",fg="white")
        self.high_label=Label(self,text="high",bg="navy",fg="white")

        self.low_wind_label=Label(self,text="low",bg="navy",fg="white")
        self.moderate_wind_label=Label(self,text="moderate",bg="navy",fg="white")
        self.medium_wind_label=Label(self,text="medium",bg="navy",fg="white")
        self.high_wind_label=Label(self,text="high",bg="navy",fg="white")

        self.low.place(x=20,y=20)
        self.moderate.place(x=20,y=50)
        self.medium.place(x=20,y=80)
        self.high.place(x=20,y=110)

        self.low_wind.place(x=20,y=170)
        self.moderate_wind.place(x=20,y=200)
        self.medium_wind.place(x=20,y=230)
        self.high_wind.place(x=20,y=260)

        self.low_label.place(x=55,y=20)
        self.moderate_label.place(x=55,y=50)
        self.medium_label.place(x=55,y=80)
        self.high_label.place(x=55,y=110)

        self.low_wind_label.place(x=55,y=170)
        self.moderate_wind_label.place(x=55,y=200)
        self.medium_wind_label.place(x=55,y=230)
        self.high_wind_label.place(x=55,y=260)

    
    def page_5(self):
        self.text=Label(self,bg="navy",fg="white",justify="left",
                text="""
                Each iteration there is a certain chance for a wind to appear.
                If a wind is generated, with another, certain chance, the wind
                will have a width of 2. Winds with a width of 2 can, again,
                with a certain chance, become winds with width 3.
                Each wind has a path reaching from one border to another.
                Each wind has a randomly picked wind force (between 1 and 12).
                Each wind has a randomly determined length (between 3 and 12 tiles).
                Each wind drags dust from regions it passes through with it,
                the amount of dust it carries depends on the wind force, with
                stronger winds holding higher amounts of dust.
                Each wind moves between 25% and 100%
                of the dust from the regions it passes through.
                The dust absorbed by the wind
                is being carried to the next tile, which the wind passes through.
                This happens for each cell the wind is currently present at.
                The winds have a more saturated colour than the rest of the cells,
                so they are easier to notice.
                The arrows represent the directions, which the winds are moving in.
                You can hide the winds by pressing "hide winds".
                """)
        self.text.place(x=120,y=10)
        wind_colour=Node.get_wind_colour(0)
        self.wind_tile=Label(self,text="↑",width=3,bg=wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.wind_tile1=Label(self,text="↑",width=3,bg=wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.wind_tile2=Label(self,text="↑",width=3,bg=wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.wind_tile3=Label(self,text="↑",width=3,bg=wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.wind_tile4=Label(self,text="↑",width=3,bg=wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.wind_tile5=Label(self,text="↑",width=3,bg=wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.wind_tile6=Label(self,text="↑",width=3,bg=wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.wind_tile7=Label(self,text="↑",width=3,bg=wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.wind_tile8=Label(self,text="↑",width=3,bg=wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.wind_tile9=Label(self,text="↑",width=3,bg=wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.wind_tile10=Label(self,text="↑",width=3,bg=wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.wind_tile11=Label(self,text="↑",width=3,bg=wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.wind_tile12=Label(self,text="↑",width=3,bg=wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.wind_tile13=Label(self,text="↑",width=3,bg=wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.wind_tile14=Label(self,text="↑",width=3,bg=wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.wind_tile15=Label(self,text="↑",width=3,bg=wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.wind_tile16=Label(self,text="↑",width=3,bg=wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)
        self.wind_tile17=Label(self,text="↑",width=3,bg=wind_colour,fg="black",relief="ridge",height=1,borderwidth=1)

        x_=30
        y_=60
        y__=200
        y___=340

        self.wind_tile.place(x=x_,y=y_)
        self.wind_tile1.place(x=x_+25,y=y_+20)
        self.wind_tile2.place(x=x_,y=y_+40)

        self.wind_tile3.place(x=x_+25,y=y__)
        self.wind_tile4.place(x=x_,y=y__)
        self.wind_tile5.place(x=x_+50,y=y__+20)
        self.wind_tile6.place(x=x_+25,y=y__+20)
        self.wind_tile7.place(x=x_+25,y=y__+40)
        self.wind_tile8.place(x=x_,y=y__+40)

        self.wind_tile9.place(x=x_+50,y=y___)
        self.wind_tile10.place(x=x_+25,y=y___)
        self.wind_tile11.place(x=x_,y=y___)
        self.wind_tile12.place(x=x_+75,y=y___+20)
        self.wind_tile13.place(x=x_+50,y=y___+20)
        self.wind_tile14.place(x=x_+25,y=y___+20)
        self.wind_tile15.place(x=x_+50,y=y___+40)
        self.wind_tile16.place(x=x_+25,y=y___+40)
        self.wind_tile17.place(x=x_,y=y___+40)

        self.w1_wind_label=Label(self,text="width 1",bg="navy",fg="white")
        self.w2_wind_label=Label(self,text="width 2",bg="navy",fg="white")
        self.w3_wind_label=Label(self,text="width 3",bg="navy",fg="white")

        self.w1_wind_label.place(x=x_,y=y_+65)
        self.w2_wind_label.place(x=x_+12,y=y__+65)
        self.w3_wind_label.place(x=x_+25,y=y___+65)

    def page_6(self):
        self.text=Label(self,bg="navy",fg="white",justify="left",
                text="""
                By clicking the "monitor region"-button
                you can observe one of the city complices
                (large city surrounded by smaller cities).
                The currently monitored complex is marked
                slightly on the map (see left).
                The graph shows
                the average fine dust concentration of the complex (y)
                for the past 100 iteration steps (x).
                By clicking "next complex" in the monitoring window
                you can iterate through each of the city complices.
                """)
        self.text.place(x=180,y=10)
        
        field_colour=Node.get_cell_colour(0)
        village_colour=Node.get_cell_colour(35)
        small_city_colour=Node.get_cell_colour(60)
        large_city_colour=Node.get_cell_colour(90)
        self.large_city1=Label(self,text="",width=3,bg=field_colour,relief="solid",height=1,borderwidth=1)
        self.small_city2=Label(self,text="",width=3,bg=field_colour,relief="solid",height=1,borderwidth=1)
        self.small_city3=Label(self,text="",width=3,bg=field_colour,relief="solid",height=1,borderwidth=1)
        self.small_city4=Label(self,text="",width=3,bg=field_colour,relief="solid",height=1,borderwidth=1)
        self.small_city5=Label(self,text="",width=3,bg=field_colour,relief="solid",height=1,borderwidth=1)
        self.small_city6=Label(self,text="",width=3,bg=field_colour,relief="solid",height=1,borderwidth=1)
        self.small_city7=Label(self,text="",width=3,bg=field_colour,relief="solid",height=1,borderwidth=1)
        self.small_city8=Label(self,text="",width=3,bg=field_colour,relief="solid",height=1,borderwidth=1)
        self.small_city9=Label(self,text="",width=3,bg=field_colour,relief="solid",height=1,borderwidth=1)
        self.village5=Label(self,text="",width=3,bg=field_colour,relief="ridge",height=1,borderwidth=1)
        self.village6=Label(self,text="",width=3,bg=field_colour,relief="ridge",height=1,borderwidth=1)
        self.village7=Label(self,text="",width=3,bg=field_colour,relief="ridge",height=1,borderwidth=1)
        self.village8=Label(self,text="",width=3,bg=field_colour,relief="ridge",height=1,borderwidth=1)
        
        self.field1=Label(self,text="",width=3,bg=field_colour,relief="ridge",height=1,borderwidth=1)
        self.field2=Label(self,text="",width=3,bg=field_colour,relief="ridge",height=1,borderwidth=1)
        self.field3=Label(self,text="",width=3,bg=field_colour,relief="ridge",height=1,borderwidth=1)
        self.field4=Label(self,text="",width=3,bg=field_colour,relief="ridge",height=1,borderwidth=1)
        self.field5=Label(self,text="",width=3,bg=field_colour,relief="ridge",height=1,borderwidth=1)
        self.field6=Label(self,text="",width=3,bg=field_colour,relief="ridge",height=1,borderwidth=1)
        self.field7=Label(self,text="",width=3,bg=field_colour,relief="ridge",height=1,borderwidth=1)
        self.field8=Label(self,text="",width=3,bg=field_colour,relief="ridge",height=1,borderwidth=1)
        self.field9=Label(self,text="",width=3,bg=field_colour,relief="ridge",height=1,borderwidth=1)
        self.field10=Label(self,text="",width=3,bg=field_colour,relief="ridge",height=1,borderwidth=1)
        self.field11=Label(self,text="",width=3,bg=field_colour,relief="ridge",height=1,borderwidth=1)
        self.field12=Label(self,text="",width=3,bg=field_colour,relief="ridge",height=1,borderwidth=1)
        

        self.m_highlight_label=Label(self,text="monitor highlighting",bg="navy",fg="white")
        
        x_=100
        y_=250
        
        self.large_city1.place(x=x_,y=y_)
        self.small_city2.place(x=x_-25,y=y_)
        self.small_city3.place(x=x_+25,y=y_)
        self.small_city4.place(x=x_,y=y_+20)
        self.small_city5.place(x=x_,y=y_-20)
        self.small_city6.place(x=x_-25,y=y_-20)
        self.small_city7.place(x=x_-25,y=y_+20)
        self.small_city8.place(x=x_+25,y=y_-20)
        self.small_city9.place(x=x_+25,y=y_+20)
        self.village5.place(x=x_,y=y_+40)
        self.village6.place(x=x_,y=y_-40)
        self.village7.place(x=x_-50,y=y_)
        self.village8.place(x=x_+50,y=y_)
        
        self.field1.place(x=x_-50,y=y_-40)
        self.field2.place(x=x_-50,y=y_-20)
        self.field3.place(x=x_-25,y=y_-40)
        
        self.field4.place(x=x_+50,y=y_-40)
        self.field5.place(x=x_+50,y=y_-20)
        self.field6.place(x=x_+25,y=y_-40)
        
        self.field7.place(x=x_-50,y=y_+40)
        self.field8.place(x=x_-50,y=y_+20)
        self.field9.place(x=x_-25,y=y_+40)
        
        self.field10.place(x=x_+50,y=y_+40)
        self.field11.place(x=x_+50,y=y_+20)
        self.field12.place(x=x_+25,y=y_+40)
        
        self.m_highlight_label.place(x=x_-45,y=y_+65)
        
        self.figure = Figure(figsize=(4,3.2),dpi=50)
        self.ax = self.figure.add_subplot(111)
        self.ax.plot([1,2,3],[3,2,5],"b-",color="#add8e6")

        self.figure.set_facecolor("navy")
        self.ax.set_facecolor("navy")
        self.ax.spines["bottom"].set_color("white")
        self.ax.spines["left"].set_color("white")
        self.ax.spines["top"].set_color("navy")
        self.ax.spines["right"].set_color("navy")
        self.ax.tick_params(axis="x", colors="white")
        self.ax.tick_params(axis="y", colors="white")
        self.ax.set_xlabel("iteration step",color="white",fontsize=8)
        self.ax.set_ylabel("fine dust concentration",color="white",fontsize=8)

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        try:
            self.canvas.show()
        except:
            self.canvas.draw()
        self.canvas.get_tk_widget().place(x=15,y=10)

    
    def page_7(self):
        self.text=Label(self,bg="navy",fg="white",justify="left",
                text="""
                You can configure some of the simulation
                settings in the 'configure params'-menu.
                Make sure to press 'update parameters'
                before closing the window.
                """)
        self.text.place(x=120,y=10)
        
    def delete_page_1(self):
        self.text1.destroy()

    def delete_page_2(self):
        self.text1.destroy()
        self.text2.destroy()
        self.field.destroy()
        self.village.destroy()
        self.village1.destroy()
        self.village2.destroy()
        self.village3.destroy()
        self.village4.destroy()
        self.village5.destroy()
        self.village6.destroy()
        self.village7.destroy()
        self.village8.destroy()
        self.small_city.destroy()
        self.small_city1.destroy()
        self.small_city2.destroy()
        self.small_city3.destroy()
        self.small_city4.destroy()
        self.small_city5.destroy()
        self.small_city6.destroy()
        self.small_city7.destroy()
        self.small_city8.destroy()
        self.small_city9.destroy()
        self.large_city.destroy()
        self.large_city1.destroy()
        self.small_complex_label.destroy()
        self.large_complex_label.destroy()
        self.field_label.destroy()
        self.village_label.destroy()
        self.small_city_label.destroy()
        self.large_city_label.destroy()
        

    def delete_page_3(self):
        self.text.destroy()
        self.village.destroy()
        self.village1.destroy()
        self.village2.destroy()
        self.village3.destroy()
        self.village4.destroy()
        self.small_city1.destroy()
        self.value_label.destroy()
        self.scatter_label.destroy()

    def delete_page_4(self):
        self.low.destroy()
        self.low_wind.destroy()
        self.low_label.destroy()
        self.low_wind_label.destroy()
        self.moderate.destroy()
        self.moderate_wind.destroy()
        self.moderate_label.destroy()
        self.moderate_wind_label.destroy()
        self.medium.destroy()
        self.medium_wind.destroy()
        self.medium_label.destroy()
        self.medium_wind_label.destroy()
        self.high.destroy()
        self.high_wind.destroy()
        self.high_label.destroy()
        self.high_wind_label.destroy()
        self.text.destroy()
        self.text2.destroy()

    def delete_page_5(self):
        self.wind_tile.destroy()
        self.wind_tile1.destroy()
        self.wind_tile2.destroy()
        self.wind_tile3.destroy()
        self.wind_tile4.destroy()
        self.wind_tile5.destroy()
        self.wind_tile6.destroy()
        self.wind_tile7.destroy()
        self.wind_tile8.destroy()
        self.wind_tile9.destroy()
        self.wind_tile10.destroy()
        self.wind_tile11.destroy()
        self.wind_tile12.destroy()
        self.wind_tile13.destroy()
        self.wind_tile14.destroy()
        self.wind_tile15.destroy()
        self.wind_tile16.destroy()
        self.wind_tile17.destroy()
        self.text.destroy()
        self.w1_wind_label.destroy()
        self.w2_wind_label.destroy()
        self.w3_wind_label.destroy()

    def delete_page_6(self):
        self.large_city1.destroy()
        self.small_city2.destroy()
        self.small_city3.destroy()
        self.small_city4.destroy()
        self.small_city5.destroy()
        self.small_city6.destroy()
        self.small_city7.destroy()
        self.small_city8.destroy()
        self.small_city9.destroy()
        self.village5.destroy()
        self.village6.destroy()
        self.village7.destroy()
        self.village8.destroy()
        
        self.field1.destroy()
        self.field2.destroy()
        self.field3.destroy()
        self.field4.destroy()
        self.field5.destroy()
        self.field6.destroy()
        self.field7.destroy()
        self.field8.destroy()
        self.field9.destroy()
        self.field10.destroy()
        self.field11.destroy()
        self.field12.destroy()

        self.text.destroy()
        self.m_highlight_label.destroy()
        matplotlib.pyplot.close(self.figure)
        self.ax.clear()
        self.ax.spines["bottom"].set_color("navy")
        self.ax.spines["left"].set_color("navy")
        self.ax.tick_params(axis="x", colors="navy")
        self.ax.tick_params(axis="y", colors="navy")
        #self.canvas.clf(keep_observers=False)
        self.canvas.draw()

    def delete_page_7(self):
        pass
        
        
        

class Monitor(Tk):
    def __init__(self,exit_command,x,y,next_complex_command):
        Tk.__init__(self)
        self.config(bg="navy")
        self.geometry("550x375")
        self.title("monitor")
        plt.tight_layout()
        
        self.figure = Figure(figsize=(6,4),dpi=80)
        self.ax = self.figure.add_subplot(111)
        self.ax.plot(x,y,"b-",color="#add8e6")

        self.figure.set_facecolor("navy")
        self.ax.set_facecolor("navy")
        self.ax.spines["bottom"].set_color("white")
        self.ax.spines["left"].set_color("white")
        self.ax.spines["top"].set_color("navy")
        self.ax.spines["right"].set_color("navy")
        self.ax.tick_params(axis="x", colors="white")
        self.ax.tick_params(axis="y", colors="white")
        self.ax.set_xlabel("iteration step",color="white",fontsize=12)
        self.ax.set_ylabel("fine dust concentration",color="white",fontsize=12)
        #self.x_label=

        #self.ax.autoscale()

        self.canvas = FigureCanvasTkAgg(self.figure, self)
        try:
            self.canvas.show()
        except:
            self.canvas.draw()
        self.canvas.get_tk_widget().place(x=20,y=0)

        #toolbar = NavigationToolbar2TkAgg(canvas, self)
        #toolbar.update()
        #canvas._tkcanvas.place(x=10,y=100)

        self.bind('<Destroy>', lambda self: exit_command())

        self.next_complex_button=Button(self,text="next complex",
                                        command=next_complex_command,bg="light blue",activebackground="light blue")
        self.next_complex_button.place(x=220,y=335)

    def refresh_figure(self,x,y):
        #print(self.ax.__dict__,self.figure.__dict__,self.canvas.__dict__)
        self.ax.cla()
        self.ax.plot(x,y)
        self.ax.set_xlabel("iteration step",color="white",fontsize=12)
        self.ax.set_ylabel("fine dust concentration",color="white",fontsize=12)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        try:
            self.canvas.show()
        except:
            self.canvas.draw()
        self.canvas.get_tk_widget().place(x=20,y=0)

class Setup(Tk):
    def __init__(self,update_command):
        Tk.__init__(self)
        self.config(bg="navy")
        self.geometry("525x460")
        self.title("setup")
        #self,dim,amounts,wind_chance,width_chances=[],n_iterations=0
        #self.dim_scale=Scale(self,from_=1,to_=50,orient="horizontal",length=343,bg="light blue",troughcolor="white",activebackground="light blue")
        self.wind_chance_scale=Scale(self,from_=0,to=100,orient="horizontal",length=343,bg="light blue",troughcolor="white",activebackground="light blue")
        self.width_chances_scale1=Scale(self,from_=0,to=100,orient="horizontal",length=345,bg="light blue",troughcolor="white",activebackground="light blue")
        self.width_chances_scale2=Scale(self,from_=0,to=100,orient="horizontal",length=346,bg="light blue",troughcolor="white",activebackground="light blue")
        self.speed_scale=Scale(self,from_=1,to=10,orient="horizontal",length=346,bg="light blue",troughcolor="white",activebackground="light blue")

        #self.growth_scale1=Scale(self,from_=-10,to=50,orient="horizontal",length=322,bg="light blue",troughcolor="white",activebackground="light blue")
        #self.growth_scale2=Scale(self,from_=-10,to=50,orient="horizontal",length=322,bg="light blue",troughcolor="white",activebackground="light blue")
        #self.growth_scale3=Scale(self,from_=-10,to=50,orient="horizontal",length=322,bg="light blue",troughcolor="white",activebackground="light blue")

        #self.limit_scale1=Scale(self,from_=-10,to=50,orient="horizontal",length=322,bg="light blue",troughcolor="white",activebackground="light blue")
        #self.limit_scale2=Scale(self,from_=-10,to=50,orient="horizontal",length=322,bg="light blue",troughcolor="white",activebackground="light blue")
        #self.limit_scale3=Scale(self,from_=-10,to=50,orient="horizontal",length=322,bg="light blue",troughcolor="white",activebackground="light blue")
        
        self.update_button=Button(self,text="update parameters",command=update_command,bg="light blue",activebackground="light blue")

        #self.dim_label=Label(self,text="dimension of the grid (x==y)",bg="light blue",padx=85)
        self.wind_chance_label=Label(self,text="wind creation chance (applied every iteration)",bg="light blue",padx=52)
        self.width_chances_label1=Label(self,text="chance for a created wind to have a width of 2",bg="light blue",padx=52)
        self.width_chances_label2=Label(self,text="chance for a created wind with a width of 2 to receive a width of 3",bg="light blue")
        self.speed_label=Label(self,text="speed of the simulation",bg="light blue",padx=112)
        #self.bar_label=Label(self,text="",height=500,font="Arial 1")
        #self.update_text=Label(self,text="",bg="navy",fg="white")

        self.wind_chance_scale.place(x=20,y=20)
        self.width_chances_scale1.place(x=20,y=120)
        self.width_chances_scale2.place(x=20,y=220)
        self.speed_scale.place(x=20,y=320)
        self.update_button.place(x=400,y=22)
        #self.dim_scale.place(x=20,y=440)
        #self.bar_label.place(x=510,y=410)

        self.wind_chance_label.place(x=20,y=63)
        self.width_chances_label1.place(x=20,y=163)
        self.width_chances_label2.place(x=20,y=263)
        self.speed_label.place(x=20,y=363)
        #self.update_text.place(x=375,y=65)
        #self.dim_label.place(x=20,y=503)

        self.highlight_winds_var=IntVar(self)
        self.highlight_winds_checkbutton=Checkbutton(self,text="disable wind highlighting",bg="light blue",activebackground="light blue",var=self.highlight_winds_var,padx=96)
        self.highlight_winds_checkbutton.place(x=20,y=415)

    def flash_update_text(self):
        try:
            self.update_text.destroy()
        except:
            pass
        
        self.update_text=Label(self,text="updated!",bg="navy",fg="white")
        self.update_text.place(x=400,y=65)

        
#class Start_up(Tk):
#    def __init__(self):
#        pass
        

    
class View(Tk):
    def __init__(self,dim,amounts,
                 step_command,auto_command,toggle_cities_command,toggle_winds_command
                 ,toggle_numbers_command,show_help_command,config_command,monitor_command):
        #amounts: [] list of int (large cities, small cities, villages)
        Tk.__init__(self)
        self.title("fine dust - wind simulation")
        #self.geometry("900x510")
        self.main_frame=Frame(self,width=780,height=508,colormap="new",bg="white",padx=2,pady=2)
        self.main_frame.grid(column=0,row=0,sticky="nsew",padx=20,pady=20)
        #self.main_frame.grid_rowconfigure(0,weight=1)
        #self.main_frame.grid_columnconfigure(0,weight=1)
        #self.pad_frame=Frame(self,width=15,height=450,bg="navy")
        #self.pad_frame.grid(row=0,column=1)
        self.config_frame=Frame(self,width=50,height=100,colormap="new",bg="navy")
        self.config_frame.grid(row=0,column=2,sticky="nsew",pady=0)#,columnspan=3,rowspan=3)
        #self.config_frame.grid_propagate(0)
        for i in range(25):
            self.main_frame.grid_rowconfigure(i,weight=1)
        for i in range(25):
            self.main_frame.grid_columnconfigure(i,weight=1)
        for i in range(8):
            self.config_frame.grid_rowconfigure(i,weight=1)
        for i in range(1):
            self.config_frame.grid_columnconfigure(i,weight=1)
        for i in range(1):
            self.rowconfigure(i,weight=1)
        for i in range(1):
            self.columnconfigure(i,weight=1)
        self.config_frame.grid_columnconfigure(i,weight=1)
        self.config(bg="navy")
        self.nodes=[]
        self.node_matrix_temp=list(np.zeros((dim,dim)))
        self.node_matrix=[]
        for node_array in self.node_matrix_temp:
            self.node_matrix.append(list(node_array))
        self.dim=dim
        for i in range(dim):
            for j in range(dim):
                node=Node(self.main_frame,"basic",i,j)
                node.grid(column=i,row=j,sticky="nsew")
                self.nodes.append(node)
                self.node_matrix[i][j]=node

        button_bg="light blue"

        self.step_button=Button(self.config_frame,text="step",command=step_command,background=button_bg,activebackground=button_bg)
        self.step_button.grid(column=0,row=0,sticky="nsew",pady=(20,20),padx=20)

        self.auto_button=Button(self.config_frame,text="start",command=auto_command,bg=button_bg)
        self.auto_button.grid(column=0,row=1,sticky="nsew",pady=(0,60),padx=20)

        self.toggle_cities_button=Button(self.config_frame,text="show cities",command=toggle_cities_command,bg=button_bg,activebackground=button_bg)
        self.toggle_cities_button.grid(column=0,row=2,sticky="nsew",pady=(0,20),padx=20)

        self.toggle_winds_button=Button(self.config_frame,text="hide winds",command=toggle_winds_command,bg=button_bg,activebackground=button_bg)
        self.toggle_winds_button.grid(column=0,row=3,sticky="nsew",pady=(0,20),padx=20)

        self.toggle_numbers_button=Button(self.config_frame,text="show numbers",command=toggle_numbers_command,bg=button_bg,activebackground=button_bg)
        self.toggle_numbers_button.grid(column=0,row=4,sticky="nsew",pady=(0,20),padx=20)

        self.show_help_button=Button(self.config_frame,text="legend/help",command=show_help_command,bg=button_bg,activebackground=button_bg)
        self.show_help_button.grid(column=0,row=5,sticky="nsew",pady=(0,40),padx=20)

        self.monitor_region_button=Button(self.config_frame,text="monitor region",command=monitor_command,bg=button_bg,activebackground=button_bg)
        self.monitor_region_button.grid(column=0,row=6,sticky="nsew",pady=(60,0),padx=20)

        self.config_button=Button(self.config_frame,text="configure params",command=config_command,bg=button_bg,activebackground=button_bg)
        self.config_button.grid(column=0,row=7,sticky="nsew",pady=20,padx=20)

        #help button
        #legend button
        
               

#--------------------Controller--------------------

class Controller(object):
    def __init__(self,dim,amounts,wind_chance,width_chances=[],n_iterations=0): #0/1 überall gleiche Bedeutung, anpassen
        print("test1.5")
        #wind_chance 0<=x<=100
        self.view=View(dim,[1],self.step,self.switch_auto,self.toggle_cities,
                       self.toggle_winds,self.toggle_numbers,self.show_help,self.configure_params,self.monitor_region)
        self.calculator=Calculator()
        self.city_coords=self.choose_cities(amounts)
        self.mark_cities2(self.city_coords)
        self.wind_chance=wind_chance
        self.width_chances=width_chances
        self.winds=[]
        self.wind_cache=[]
        self.wind_cache_lengths=[]
        self.finished_winds=[]
        self.auto=0 #0: False, 1:True
        self.show_numbers=0
        self.show_cities=0
        self.show_winds=1
        self.track_complices_flag=0
        self.highlight_winds=0
        self.monitor_flag=1
        self.monitor_index=None
        self.city_complices=self.get_city_complices()
        self.city_complices_cache=[ [] for i in range(len(self.city_complices))]
        self.current_iteration=0
        self.waiting_time=0.2
        self.mainloop()
        
    def mainloop(self):
        while self.auto==1:
           # self.check_auto()
            self.view.update_idletasks()
            self.view.update()
            self.step()
            #print("e")
            sleep(self.waiting_time)

    def switch_auto(self):
        if self.auto==1:
            self.view.auto_button.configure(text="start")
            self.auto=0
        else:
            self.view.auto_button.configure(text="stop")
            self.auto=1
            self.mainloop()

    def check_auto(self):
        self.auto=self.auto

    def step(self):
        self.current_iteration+=1
        for node in self.view.nodes:
            node.iterate(self.show_numbers,self.current_iteration)
            coords=node.coords
            if node.value>Node.value_limits[1]: #medium/high levels scatter
                new_coords=[]
                if coords[0]<self.view.dim-1:
                    new_coords.append([coords[0]+1,coords[1]])
                if coords[1]<self.view.dim-1:
                    new_coords.append([coords[0],coords[1]+1])
                if coords[0]>0:
                    new_coords.append([coords[0]-1,coords[1]])
                if coords[1]>0:
                    new_coords.append([coords[0],coords[1]-1])

                if node.value>Node.value_limits[2]:
                    scatter=0.03
                else:
                    scatter=0.02

                for i in range(len(new_coords)):
                    n_coords=new_coords[i]
                    try:
                        old_value=self.view.node_matrix[n_coords[0]][n_coords[1]].value
                    except:
                        print(n_coords)
                    new_value=int(old_value+node.value*scatter)
                    self.view.node_matrix[n_coords[0]][n_coords[1]].value=new_value
                    if self.show_numbers==1:
                        self.view.node_matrix[n_coords[0]][n_coords[1]].config(text=new_value)

                for i in range(4):
                    node.value=int(node.value-node.value*scatter)
                    
        if self.show_cities==1:
            self.mark_cities2(self.city_coords,colourise=0)            
        #self.update_monitor()
        
        chance=np.random.randint(0,101)
        if chance<self.wind_chance*100:
            self.add_wind()
            #print("eeeee")
        if len(self.winds)!=0 and len(self.wind_cache)>0:
            self.wind_step()

        self.update_monitor()
        
        
    def choose_cities(self,amounts):
        #amounts: [x,y,z] large,small,villages
        large_cities=[]
        small_cities=[]
        villages=[]
        while len(large_cities)<amounts[0]:
            maxima=self.view.dim-2
            coords = [ np.random.randint(2,maxima), np.random.randint(2,maxima) ]
            if not coords in large_cities:
                large_cities.append(coords)
                neighbours=self.calculator.get_neighbours(coords,"large city",maxima)
                small_cities.extend(neighbours[0])
                villages.extend(neighbours[1])
                
        while len(small_cities)<amounts[1]:
            maxima=self.view.dim-1
            coords = [ np.random.randint(1,maxima), np.random.randint(1,maxima) ]
            if not coords in small_cities:
                small_cities.append(coords)
                neighbours=self.calculator.get_neighbours(coords,"small city",maxima)
                villages.extend(neighbours[1])

        while len(villages)<amounts[2]:
            maxima=self.view.dim
            coords = [ np.random.randint(0,maxima), np.random.randint(0,maxima) ]
            if not coords in villages:
                villages.append(coords)

        return (large_cities,small_cities,villages)

    def mark_cities(self,coordslist):
        #coordslist: [ [], [], [] ] #large,small,village
        for node in self.view.nodes:
            if node.coords in coordslist[0]:
                #node.config(bg="red")
                node.configure_type("large city")
            elif node.coords in coordslist[1]:
                #node.config(bg="brown")
                node.configure_type("small city")
            elif node.coords in coordslist[2]:
                #node.config(bg="cyan")
                node.configure_type("village")
            else:
                node.config(bg="green")

    def mark_cities2(self,coordslist,colourise=1): #colours - different cmap
        for coords in coordslist[2]:
            node=self.view.node_matrix[coords[0]][coords[1]]
            node.configure_type("village")
            if colourise==0:
                colour=node.get_city_colour(node.type)
                node.config(bg=colour,fg=colour)
                if self.show_numbers==1:
                    node.config(fg="white")
                    
        for coords in coordslist[1]:
            node=self.view.node_matrix[coords[0]][coords[1]]
            node.configure_type("small city")
            if colourise==0:
                colour=node.get_city_colour(node.type)
                node.config(bg=colour,fg=colour)
                if self.show_numbers==1:
                    node.config(fg="white")
                    
        for coords in coordslist[0]:
            node=self.view.node_matrix[coords[0]][coords[1]]
            node.configure_type("large city")
            if colourise==0:
                colour=node.get_city_colour(node.type)
                node.config(bg=colour,fg=colour)
                if self.show_numbers==1:
                    node.config(fg="white")

    def toggle_cities(self): #keep cities visible #show winds
        if self.show_cities==0:
            self.view.toggle_cities_button.config(text="hide cities")
            self.show_cities=1
            for node in self.view.nodes:
                node.config(bg="DarkSeaGreen1")
            self.mark_cities2(self.city_coords,colourise=0)
        else:
            self.show_cities=0
            self.view.toggle_cities_button.config(text="show cities")
            for node in self.view.nodes:
                colour=Node.get_cell_colour(node.value)
                node.config(bg=colour)
                if self.show_numbers==0:
                    node.config(fg=colour)
                else:
                    node.config(fg="black")

    def toggle_winds(self):
        if self.show_winds==1:
            self.view.toggle_winds_button.config(text="show winds")
            self.show_winds=0
            for coords_list in self.wind_cache:
                for coords in coords_list:
                    node=self.view.node_matrix[coords[0]][coords[1]]
                    colour=Node.get_cell_colour(node.value)
                    node.config(bg=colour)
                    node.config(text=node.value)
                    if self.show_numbers==0:
                        node.config(fg=colour)
        else:
            self.view.toggle_winds_button.config(text="hide winds")
            self.show_winds=1
            i=0
            for coords_list in self.wind_cache:
                for coords in coords_list:
                    node=self.view.node_matrix[coords[0]][coords[1]]
                    movement=self.winds[i].movement
                    arrow=self.calculator.get_arrow(movement)
                    if self.highlight_winds==0:
                        colour=Node.get_wind_colour(node.value)
                        node.config(bg=colour)
                    node.config(text=arrow)
                    if node.value<node.value_limits[2]:
                        node.config(fg="black")
                    else:
                         node.config(fg="white")
                i+=1
            

    def toggle_numbers(self): #change fg colours, show values of winds
        if self.show_numbers==0:
            self.show_numbers=1
            self.view.toggle_numbers_button.config(text="hide numbers")
            for node in self.view.nodes:
                node.config(fg="black",text=node.value)
                if node.value>node.value_limits[2] or (self.show_cities and node.type!="basic"):
                    node.config(fg="white")
        else:
            self.show_numbers=0
            self.view.toggle_numbers_button.config(text="show numbers")
            for node in self.view.nodes:
                colour=Node.get_cell_colour(node.value)
                node.config(fg=colour)
                
    #def toggle_wind_highlighting(self):
    #    if self.highlight_winds==0:
    #        self.highlight_winds=1
    #    else:
    #        self.highlight_winds=0
            

    def show_help(self):
        self.help=Help()

    def update_params(self):
        #self,dim,amounts,wind_chance,width_chances=[],n_iterations=0
        #dim=self.setup.dim_scale.get()
        wind_chance=self.setup.wind_chance_scale.get()/100
        width_chance1=self.setup.width_chances_scale1.get()/100
        width_chance2=self.setup.width_chances_scale2.get()/100
        speed=self.setup.speed_scale.get()
        highlight_winds=self.setup.highlight_winds_var.get()
        #print(highlight_winds)

        #self.dim
        self.wind_chance=wind_chance
        self.width_chances=[width_chance1,width_chance2]
        speed_to_waiting_time=[1,0.9,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.01]
        waiting_time=speed_to_waiting_time[speed]
        self.waiting_time=waiting_time
        self.setup.flash_update_text()
        self.highlight_winds=highlight_winds

    def configure_params(self):
        self.setup=Setup(self.update_params)
        

    def get_city_complices(self,coords_list=None):
        city_complices=[]
        if coords_list==None:
            coords_list=self.city_coords[0]
        for i in range(len(coords_list)):
            inner_city=coords_list[i]
            outer_cells=self.calculator.get_neighbours(inner_city,"city complex",self.view.dim)[1]
            outer_cells.append(inner_city)
            city_complex_coords=outer_cells[:]
            city_complex_coords.append(inner_city)
            city_complex=[]
            for coords in city_complex_coords:
                node=self.view.node_matrix[coords[0]][coords[1]]
                city_complex.append(node)
            city_complices.append(city_complex)
            
        return city_complices

    def track_complices(self):
        i=0
        for city_complex in self.city_complices:
            average_value=0
            for node in city_complex:
                average_value+=node.value
            average_value=int(average_value/9) #9= 3x3 square (city complex around large city)
            if len(self.city_complices_cache[i])>100:
                self.city_complices_cache[i].pop(0)
            self.city_complices_cache[i].append(average_value)
            i+=1
            
    def mark_monitor_region(self,city_complices=None,monitor_index=None): #let city complex blink (red colour flash)
        if city_complices==None:
            city_complices=self.city_complices
        if monitor_index==None:
            monitor_index=np.random.randint(0,len(city_complices))
        monitor_complex=city_complices[monitor_index]
        for node in monitor_complex:
            node.config(relief="solid")

        self.monitored_region=monitor_complex
        self.monitor_index=monitor_index

    def unmark_monitor_region(self):
        self.track_complices_flag=1
        self.monitor_flag=1
        for node in self.monitored_region:
            node.config(relief="ridge")
        
    def monitor_region(self): #track when button pressed / at start
        self.track_complices_flag=0
        self.monitor_flag=0
        self.mark_monitor_region()
        self.monitor=Monitor(self.unmark_monitor_region,[0],[0],self.monitor_iterate_complex)

    def monitor_iterate_complex(self):
        monitor_index=self.monitor_index+1
        if monitor_index==len(self.city_complices):
            monitor_index=0
        self.monitor_index=monitor_index
        self.unmark_monitor_region()
        self.mark_monitor_region(monitor_index=monitor_index)
        self.monitor_flag=0
        self.track_complices_flag=0
        self.update_monitor()


    def update_monitor(self):
        if self.track_complices_flag==0:
            self.track_complices()
            if self.monitor_flag==0:
                x=[]
                y=[]
                for i in range(0,100):#(self.current_iteration-3,self.current_iteration):
                    if i<0:
                        continue
                    try:
                        y.append(self.city_complices_cache[self.monitor_index][i])
                        if self.current_iteration>100:
                            x.append(range(self.current_iteration-100,self.current_iteration)[i])
                        else:
                            x.append(i)
                    except:
                        pass
                        
                self.monitor.refresh_figure(x,y)
        
            
    def add_wind(self):
        """
        movement: help list
        first entry shows which coord (column/row) shall be increased (0/1)
        second entry shows if coord shall be increased or decreased
        third/fourth entry shows whether a left/right movement is positive/negative

        border_values: help list
        values of the borderlines [col_values, row_values]
        
        """
        intensity=np.random.randint(0,13)
        maxima=self.view.dim-1
        start_coords= [ np.random.randint(0,maxima), np.random.randint(0,maxima) ]
        border=np.random.randint(0,4)
        
        if border==0:
            start_coords[0]=0
            movement=[0,1,-1,1]
            border_values=[ [maxima], [0,maxima] ]
            
        elif border==1:
            start_coords[1]=0
            movement=[1,1,1,-1]
            border_values=[ [0,maxima], [maxima] ]
            
        elif border==2:
            start_coords[0]=maxima
            movement=[0,-1,1,-1]
            border_values=[ [0], [0,maxima] ]
            
        elif border==3:
            start_coords[1]=maxima
            movement=[1,-1,-1,1]
            border_values=[ [0,maxima], [0] ]
            
        left_chance=np.random.randint(0,101)
        #right_chance=1-left_chance
        #print("uuuu")

        path=self.calculator.calculate_wind_path(start_coords,left_chance,maxima,movement,border_values)
        amplitude=np.random.randint(1,13)
        wind=Wind(path,amplitude,movement)
        self.winds.append(wind)
        self.wind_cache.append([])
        self.wind_cache_lengths.append(np.random.randint(3,12))
        self.finished_winds.append(0)

        increase_width=np.random.randint(0,100)
        if increase_width<self.width_chances[0]*100:
            increase_width=np.random.randint(0,100)
            #print(increase_width)
            if increase_width<self.width_chances[1]*100:
                #print("damn?")
                expand=2
            else:
                expand=1
                
            paths=self.calculator.expand_wind(path,expand,self.view.dim,movement)
            #print(len(paths),"lll")
            for exp_path in paths:
                wind=Wind(exp_path,amplitude,movement)
                self.winds.append(wind)
                self.wind_cache.append([])
                self.wind_cache_lengths.append(self.wind_cache_lengths[-1])
                self.finished_winds.append(0)

    def wind_step(self):
        shift=0
        i=0
        while i<len(self.winds):
            i-=shift
            if len(self.winds)==0:
                return
            #print(i,len(self.winds),shift)
            wind=self.winds[i]
            next_coords=wind.get_next_position()
            if next_coords!=None:
                self.wind_cache[i].append(next_coords)
            else:
                self.finished_winds[i]=1

            if len(self.wind_cache[i])==0:
                self.winds.pop(i)
                self.wind_cache.pop(i)
                self.wind_cache_lengths.pop(i)
                self.finished_winds.pop(i)
                #shift-=1
                i-=shift
        
            #print(i,self.wind_cache,self.wind_cache_lengths,self.finished_winds)
            elif len(self.wind_cache[i])>self.wind_cache_lengths[i] or self.finished_winds[i]==1: #3=cache size
                self.wind_cache[i].pop(0)
                #shift-=1
                i-=shift
            i+=1
        q=-1 #only for arrows        
        for coords_list in self.wind_cache:
            q+=1
            #print(q,len(self.wind_cache),len(self.winds))
            for coords in coords_list:
                if coords!=-1 and coords!=None:
                    node=self.view.node_matrix[coords[0]][coords[1]]
                    #print(coords)
                    #print(q,len(self.wind_cache),len(self.winds),"zzz")
                    level= self.view.node_matrix[coords[0]][coords[1]].value
                    if self.highlight_winds==0:
                        colour=Node.get_wind_colour(level)
                    else:
                        colour=Node.get_cell_colour(level)
                    if self.show_winds==1:
                        self.view.node_matrix[coords[0]][coords[1]].config(bg=colour)
                    movement=self.winds[q].movement
                    arrow=self.calculator.get_arrow(movement)
                    
                    if self.show_numbers==0 and self.show_winds==1:
                        node.config(text=arrow)
                    elif self.show_winds==1:
                        node.config(text=node.value)
                    
                    if node.value<node.value_limits[2] and self.show_winds==1:
                        node.config(fg="black")
                    elif self.highlight_winds==1 and self.show_winds==1:
                        node.config(fg="white")
                    

                    #if 

                else:
                    continue
                    index=self.wind_cache.index(coords_list)
                        
                    if len(self.wind_cache[index])==0:
                        self.winds.pop(index)
                        self.wind_cache.pop(index)
                        self.wind_cache_lengths.pop(index)
                        q-=1
                    elif len(self.wind_cache[index])==1:
                        self.view.node_matrix[self.wind_cache[index][0]][self.wind_cache[index][1]].value=0
                        #self.view.node_matrix[self.wind_cache[index][0]][self.wind_cache[index][1]].config(text=0)
                    else:
                        try:
                            self.wind_cache[index].pop(index) #irrelevant?
                        except:
                            print(index,self.wind_cache)
        l=0 #wind-counter
        if True:
            while l<len(self.wind_cache):
                k=0 #coord-counter
                #print(l,k,self.wind_cache,len(self.wind_cache),len(self.wind_cache[l]))
                if len(self.wind_cache[k])>1:
                    while k<len(self.wind_cache[l])-1:
                        #print(l,k,self.wind_cache,len(self.wind_cache),len(self.wind_cache[l]))
                        #print(k)
                        col=self.wind_cache[l][k][0]
                        row=self.wind_cache[l][k][1]
                        next_col=self.wind_cache[l][k+1][0]
                        next_row=self.wind_cache[l][k+1][1]

                        node=self.view.node_matrix[col][row]
                        next_node=self.view.node_matrix[next_col][next_row]

                        #node.config(bg="yellow")
                        #next_node.config(bg="black")
                        
                        value=node.value
                        #print("VALUE",value)
                        next_value=next_node.value
                        amplitude=self.winds[l].amplitude
                        amp_to_percentage=np.linspace(50,100,13)
                        percentage=amp_to_percentage[amplitude]/100

                        #print(value,next_value,percentage)

                        new_value=int(next_value+value*percentage)
                        next_node.value=new_value

                        #print(new_value)
                        
                        #next_node.config(text=new_value) #value
                        node.value=int(value-value*percentage)
                        #node.config(text=node.value) #text

                        #scattering
                        next_neighbours=self.calculator.get_neighbours(next_node.coords,"wind cell",self.view.dim)[1]
                        #print(next_neighbours)

                        for coords in next_neighbours:
                            #print(coords)
                            try:
                                new_value=int((percentage/4)*next_node.value+self.view.node_matrix[coords[0]][coords[1]].value)
                            except:
                                print(coords)
                            next_node.value=int(next_node.value-next_node.value*(percentage/4)) #text update missing
                            self.view.node_matrix[coords[0]][coords[1]].value=new_value
                            #self.view.node_matrix[coords[0]][coords[1]].config(bg="black") #activate in debug
                            #text update missing (method that updates value and text? xd)
                        for i in range(4-len(next_neighbours)): #maybe deactivate
                            next_node.value=int(next_node.value-next_node.value*(percentage/4))
                        
                        
                        k+=1
                l+=1
            

if __name__=="__main__":
    c=Controller(25,[5,55,82],0.4,[0.5,0.25],0)
    c.view.mainloop()

