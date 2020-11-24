#Sistema de escuelas por Jenifer
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship

###############Creación de la base de datos #########################################
engine=create_engine('sqlite:///:memory:')
Base=declarative_base(engine)

class Estudiante(Base):
    __tablename__="alumno"   
    id=Column(Integer,Sequence('alumno_seq_id'),primary_key=True)
    cedula_identidad=Column(String)
    nombre_alumno=Column(String)
    apellido_alumno=Column(String)
    curso_idAlumno=Column(Integer,ForeignKey('curso.id'))
    
    cursos=relationship("Curso",back_populates='estudiantes')

    def __repr__(self):
        return'{}{}'.format(self.nombre_alumno, self.apellido_alumno)

class Curso(Base):
    __tablename__='curso'
    id=Column(Integer, Sequence('curso_seq_id'),primary_key=True)
    nombre_curso=Column(String)
        
    estudiantes=relationship("Estudiante",back_populates='cursos')
    hora_curso=relationship("Horarios",back_populates='curso_hora')
    def __repr__(self):
        return'{}'.format(self.nombre_curso)

class Horarios(Base):
    __tablename__='horario'
    id=Column(Integer, Sequence('horario_seq_id'),primary_key=True)
    dia=Column(String)
    hora_inicio=Column(String)
    hora_fin=Column(String)
    profesor_id=Column(Integer,ForeignKey('profesor.id'))
    curso_id=Column(Integer,ForeignKey('curso.id'))
    
    curso_hora=relationship("Curso",back_populates='hora_curso')
    curso_profe=relationship("Profesor",back_populates='profe_curso')

    def __repr__(self):
        return'{}{}{}'.format(self.dia,self.hora_inicio, self.hora_fin,\
        self.cedula_identidad)

class Profesor(Base):
    __tablename__='profesor'
    id=Column(Integer, Sequence('profesor_seq_id'),primary_key=True)
    cedula_identidad=Column(String)    
    nombre_profesor=Column(String)
    apellido_profesor=Column(String)
    
    profe_curso=relationship("Horarios",back_populates='curso_profe')
    def __repr__(self):
        return'{}{}{}'.format(self.nombre_profesor, self.apellido_profesor,
        self.cedula_identidad)


Profesor.__table__
Estudiante.__table__
Curso.__table__
Horarios.__table__
Base.metadata.create_all(engine)
#########################################################################################

##############Definiciones de cada funcion################################

#######################Ésta función Chequea si está el profesor en la DB#######################################
def estaProfesor(ses,identidad,nombre,apellido):
    query = ses.query(Profesor).filter(Profesor.cedula_identidad == identidad)
    query2 = ses.query(Profesor).filter(Profesor.nombre_profesor.like(nombre),Profesor.apellido_profesor.like(apellido))
    instance1 = ses.execute(query)
    instance2 = ses.execute(query2)
    
    for i in instance1:
        if i != []:
            print("El profesor ya se encuentra en la base de datos:")
            print("CI: {} Nombre: {} Apellido: {}".format(i[1],i[2],i[3]))
            return True
    for i in instance2:
        if i != []:
            print("El profesor ya se encuentra en la base de datos:")
            print("CI: {} Nombre: {} Apellido: {}".format(i[1],i[2],i[3]))
            return True
    
    return False #si el profesor está en un momento de alguno de los for, hace el return True y sale de la función 


#######################Ésta función Chequea si está el alumno en la DB#######################################  
def estaAlumno(ses,identidad,nombre,apellido):
    query = ses.query(Estudiante).filter(Estudiante.cedula_identidad == identidad)
    query2 = ses.query(Profesor).filter(Estudiante.nombre_estudiante.like(nombre),Estudiante.apellido_estudiante.like(apellido))
    instance1 = ses.execute(query)
    instance2 = ses.execute(query2)
    
    for i in instance1:
        if i != []:
            print("El estudiante ya se encuentra en la base de datos:")
            print("CI: {} Nombre: {} Apellido {}".format(i[1],i[2],i[3]))
            return True
    for i in instance2:
        if i != []:
            print("El estudiante ya se encuentra en la base de datos:")
            print("CI: {} Nombre: {} Apellido: {}".format(i[1],i[2],i[3]))
            return True
    
    return False #si el alumno está en un momento de alguno de los for, hace el return True y sale de la función 
###############################################################################

#######################Ésta función Chequea si está el curso en la DB#######################################
def estaCurso(ses,nom_curso):
    nom_curso = nom_curso.capitalize()
    query = ses.query(Curso).filter(Curso.nombre_curso.like(nom_curso))
    instance = ses.execute(query)
    for i in instance:
        if i != []:
            return True
    
    return False
###############################################################################


#######################Ésta función Agrega a un nuevo profesor#######################################
def agregarProfesor (ses):
    identidad= input("Ingrese el numero de identidad del profesor:")
    nombre = input("Ingrese Solo el Nombre del Profesor:")
    apellido = input("Ingrese solo el Apellido del Profesor:")
    if not estaProfesor(ses, identidad, nombre, apellido):
        prof_nuevo = Profesor(nombre_profesor=nombre, apellido_profesor=apellido,\
                              cedula_identidad=identidad)

        ses.add(prof_nuevo)
        ses.commit()
##################################################################################################
            
#######################Ésta función Agrega a un nuevo Curso#######################################
def agregarCurso(ses):
    nombre_cur= input("Ingrese el nombre del curso:")
    if not estaCurso(ses, nombre_cur):
          curso_nuevo = Curso(nombre_curso=nombre_cur)
          #acá hace falta agregar los horarios
          
          ses.add(curso_nuevo)
          ses.commit()
    else:
          print("El curso {} ya existe".format(nombre_cur))

            
#######################Ésta función Agrega a un nuevo Alumno#######################################
def agregarAlumno(ses):
    identidad= input ("Ingrese el numero de identidad del estudiante:")
    nombre = input("Ingrese Solo el Nombre del Estudiante:")
    apellido = input("Ingrese solo el Apellido del Estudiante:")
    if not estaAlumno(ses, identidad, nombre, apellido):
        estud_nuevo = Estudiante(nombre_estudiante=nombre, apellido_estudiante=apellido,\
                              cedula_identidad=identidad)
        ses.add(estud_nuevo)
        ses.commit()
##################################################################################################

def asignarAlumnoACurso(ses):
    
    print("Asignar estudiante a curso")

def asignarProfesorACurso(ses):
    print("Asignar profesor a curso")
#algo aca

def asignarHorarioProfCurso(ses):
    return None


#########################Exporta a un archivo csv los datos de profesor, alumno, curso y hora#################################
def exportarAlumnosPerteneceACurso(ses):
    salida = input("Escriba el nombre del archivo SIN LA EXTENSIÓN: ")
    salida= salida + '.csv'
    select_profesor = select('*').select_from(Profesor)
    select_alumno   = select('*').select_from(Alumnos)
    select_curso    = select('*').select_from(Curso)
    select_horario  = select('*').select_from(Horario)
    res_prof        = ses.execute(select_profesor).fetchall()
    res_al          = ses.execute(select_alumno).fetchall()
    res_cur         = ses.execute(select_curso).fetchall()
    res_hor         = ses.execute(select_horario).fetchall()
    try:
        with open(salida, 'w') as f: 
            csv_out = csv.writer(f)
            for row in res_prof, res_al, res_cur, res_hor:
                csv_out.writerow(row)
    except Exception as e:
        print (e)  
##############################################################################


###############################################################################
#Ésta función es para precargar datos en las DB #
#Si ne se quiere eso, comente la linea que llama a esta función en el main y listo
def precargarDatos(ses):
###############ESTUDINTES##################################################
    alumno1=Estudiante(nombre_alumno='Raton', apellido_alumno='Perez',
    cedula_identidad='1234567-8')
    alumno2=Estudiante(nombre_alumno='Hugo', apellido_alumno='Donald',\
    cedula_identidad='abcdef123')
    alumno3=Estudiante(nombre_alumno='Paco', apellido_alumno='Donald',\
    cedula_identidad='abcdef124')
    alumno4=Estudiante(nombre_alumno='Luis', apellido_alumno='Donald',\
    cedula_identidad='abcdef125')
    ses.add(alumno1)
    ses.add(alumno2)
    ses.add(alumno3)
    ses.add(alumno4)
############PROFESORES###################################################
    prof1= Profesor(nombre_profesor='Profesor1', apellido_profesor='El 1',\
    cedula_identidad='1234567-9')
    prof2= Profesor(nombre_profesor='Profesor1', apellido_profesor='El 2',\
    cedula_identidad='1234567-10')
    prof3= Profesor(nombre_profesor='Profesor3', apellido_profesor='El 3',\
    cedula_identidad='1234567-11')
    ses.add(prof1)
    ses.add(prof2)
    ses.add(prof3)

#######################Horarios#######################################



#######################Cursos#######################################
    fisica=Curso(nombre_curso="Fisica",estudiantes=[alumno1,alumno2])
    quimica=Curso(nombre_curso="Quimica", estudiantes=[alumno3])
    biologia=Curso(nombre_curso="Biología", estudiantes=[alumno4])
    ses.add(fisica)
    ses.add(quimica)
    ses.add(biologia)
    
    ses.commit()
####################################################################################################


#############Funcion que despliega el menú##########################################################
def impr_op_posibles():
  print("Estas son las operaciones  que se pueden hacer")
  print("1 - agregar alumno")
  print("2 - agregar curso")
  print("3 - agregar profesor")
  print("4 - asignar un alumno a un curso")
  print("5 - asignar un profesor a un curso")
  print("6 - asignar un horario a un profesor de un curso")
  print("7 - imprime en un archivo en formato csv, los alumnos y los profesores con sus horarios")
  print("8 - salir")
  
print("Bienvenidos al sistema de escuela")

def ingresar_operacion():
    opcion = 0
    try:
        impr_op_posibles()
        opcion = int(input("Elije una opcion (con numeros)"))

        if opcion < 1 or opcion > 8:
            print("##################################")
            print("ingresa un numero valido por favor")
            print("##################################")
            ingresar_operacion()

    except ValueError:
        print("##################################")
        print("ingresa un numero valido por favor")
        print("##################################")
        ingresar_operacion()

    return opcion

def realizar_operacion(operacion, session):
    if (operacion == 8):
        session.close()

    elif (operacion ==1):
        agregarAlumno(session)

    elif (operacion ==2):
        agregarCurso(session)

    elif (operacion ==3):
        agregarProfesor(session)

    elif (operacion == 4):
        asignarAlumnoACurso(session)

    elif (operacion == 5):
        asignarProfesorACurso(session)

    elif (operacion == 6):
        asignarHorarioProfCurso(session)

    elif (operacion == 7):
        exportarAlumnosPerteneceACurso(session)
    else:
        print("Operación no válida")

 

#############Main#############################################################
def main():
    Session = sessionmaker(bind=engine)
    session = Session()

    operacion = 0
    precargarDatos(session)
    while operacion != 8:
        operacion = ingresar_operacion()
        realizar_operacion(operacion, session)

    print ("Gracias por usar nuestro sistema de escuela")

if __name__ == '__main__':
    main()