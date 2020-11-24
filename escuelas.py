from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, Sequence, ForeignKey, select
from sqlalchemy.orm import relationship,sessionmaker
import csv
Base   = declarative_base()
engine  = create_engine('sqlite:///:memory:')

class Horario(Base):
    __tablename__         = "horario"
    identificadorCurso    = Column(Integer, ForeignKey("curso.id_curso"),primary_key=True)
    identificadorProfesor = Column(Integer, ForeignKey("profesor.id_profesor"),primary_key=True)

class Curso(Base):
    __tablename__ = "curso"
    id_curso      = Column(Integer, Sequence("id_curso"), primary_key=True)
    nombreCurso   = Column(String)
    horaCurso     = Column(Integer)
    alumno        = relationship("Alumnos", back_populates="curso")
    cursoProf     = relationship("Profesor", secondary="horario")

    def __repr__(self):
        return "{} {} {}".format(self.id_curso, self.nombreCurso, self.horaCurso)

class Profesor(Base):
    __tablename__     = "profesor"
    id_profesor       = Column(Integer, Sequence("id_profesor"), primary_key=True)
    nombreProfesor    = Column(String)
    apellidoProfesor  = Column(String)
    profCurso         = relationship("Curso",secondary="horario")

    def __repr__(self):
        return "{} {} {}".format(self.id_profesor,self.nombreProfesor,self.apellidoProfesor)

class Alumnos(Base):
    __tablename__   = "alumnos"
    id_alumno       = Column(Integer, Sequence("id_alumno"), primary_key=True)
    nombreAlumno    = Column(String)
    apellidoAlumno  = Column(String)
    cursoAlumno     = Column(Integer, ForeignKey("curso.id_curso"))
    curso           = relationship("Curso", back_populates="alumno")

    def __repr__(self):
        return "{} {} {} {}".format(self.id_alumno, self.nombreAlumno,
                                    self.apellidoAlumno, self.cursoAlumno)

def no_hayCursos():
    if sesion.query(Curso).order_by(Curso.id_curso).all():
        return False
    else:
        print("################################")
        print("no hay cursos genere uno antes:")
        return True
def mostrarMenu():
    print("                                                         ")
    print("***********  SISTEMA PARA ESCUELAS  ***************")
    print("                                                         ")
    print("REGISTRO             | CONSULTA     ")
    print("1 - Cursos           | 4 - Alumnos de un curso   ")
    print("2 - Profesores       | 5 - Horario de un profesor")
    print("3 - Alumnos          | 6 - Horario de un curso   ")
    print("             7 - Exportar datos")
    print("             8 - Finalizar Sesion                              ")
    regist = " "
    while regist not in {"1","2","3","4","5","6","0","7"}:
         regist = input("Seleccione una opcion valida")
    return int(regist)

def altaCurso():
    global sesion
    print("                                                       ")
    nombreCur = (input("Introduzca el nombre del curso: "))
    print("                                              ")
    print("HORARIOS:")
    print("1- 8:00h a 9:00h")
    print("2- 9:00h a 10:00h")
    print("3- 11:00h a 12:00h")
    print("4- 12:00h a 13:00h")
    horaCur = " "
    while horaCur not in {"1","2","3","4"}:
        horaCur = input("Introduzca un horario para el curso: ")
    if   horaCur == "1": h = 8
    elif horaCur == "2": h = 9
    elif horaCur == "3": h = 11
    elif horaCur == "4": h = 12
    curso1 = Curso ( nombreCurso = nombreCur, horaCurso = h)
    sesion.add(curso1)
    sesion.commit()
    print("* El curso ", nombreCur, " se ha dado de alta *")

def altaProfesor():
    global sesion
    if no_hayCursos():
        print("################################")
        aplic()
    print("                                                       ")
    nombreProf = input("Introduzca el nombre del profesor: ")
    apellidoProf = input("Introduzca el apellido del profesor: ")
    profesor1 = Profesor(nombreProfesor=nombreProf, apellidoProfesor=apellidoProf)
    sesion.add(profesor1)
    print("                                                          ")
    print("Asocie el profesor a un curso. Estos son nuestros cursos:")
    for instancia in sesion.query(Curso).order_by(Curso.id_curso):
        print(instancia.id_curso, instancia.nombreCurso, instancia.horaCurso)
    while True:
        try:
            numeroCurso = sesion.query(Curso).order_by(Curso.id_curso).count()
            selec = int(input(" seleccione el numero del curso del profesor"))
            if numeroCurso >= selec:
                cur = sesion.query(Curso).filter(Curso.id_curso == selec).one()
                profesor1.profCurso.append(cur)
                sesion.commit()
                print("* El Profesor ", nombreProf, apellidoProf, "se ha dado de alta *")
                break
            else:
                print("opcion incorrecta")
                continue
        except ValueError:
            print("El valor introducido es erroneo")
            continue

def altaAlumno():
    global sesion
    if no_hayCursos():
        print("################################")
        aplic()
    print("                                                       ")
    nombreAlum = input("Introduzca el nombre del Alumno: ")
    apellidoAlum = input("Introduzca el apellido del Alumno: ")
    print("                                                       ")
    print("Asocie el alumno a un curso. Estos son nuestros cursos:")
    for instancia in sesion.query(Curso).order_by(Curso.id_curso):
        print(instancia.id_curso, instancia.nombreCurso)
    while True:
        try:
            cursoAlum = int(input("seleccione el numero del curso del Alumno"))
            numeroCurso = sesion.query(Curso).order_by(Curso.id_curso).count()
            if numeroCurso >= cursoAlum:
                alumno1 = Alumnos(nombreAlumno=nombreAlum, apellidoAlumno=apellidoAlum, cursoAlumno=cursoAlum)
                sesion.add(alumno1)
                sesion.commit()
                print(" * El alumno: ", nombreAlum," ", apellidoAlum, " se ha dado de alta * ")
                break
            else:
                print("opcion incorrecta")
                continue
        except ValueError:
            print("El valor introducido es erroneo")
            continue


def horarioProfesor():
    global sesion
    if no_hayCursos():
        print("################################")
        aplic()
    print("                         ")
    print("------ HORARIOS DE UN PROFESOR  ---------")
    print("                         ")
    print("Estos son nuestros profesores")
    if not no_hayCursos:
        aplic()
    for instancia in sesion.query(Profesor).order_by(Profesor.id_profesor):
        print(instancia.id_profesor, instancia.nombreProfesor, instancia.apellidoProfesor)
    print()
    while True:
        try:
            consProf   = int(input("seleccione el identificador del profesor para ver su horario"))
            numeroProf = sesion.query(Profesor).order_by(Profesor.id_profesor).count()
            if numeroProf >= consProf:
                otraquery = sesion.query(Curso).filter(Curso.cursoProf.any(Profesor.id_profesor == consProf)).all()
                print("El horario de este profesor es:")
                for n in otraquery:
                    print("Hora: {}:00h   Curso: {}".format(n.horaCurso,n.nombreCurso))
                break
            elif numeroProf < consProf:
                print("opcion incorrecta")
                continue

        except ValueError:
            print("El valor introducido no es correcto")

def horarioCurso():
    global sesion
    if no_hayCursos():
        print("################################")
        aplic()
    print("                         ")
    print("------  HORARIOS CURSOS  ------------------")
    print("                         ")
    print("Estos son nuestros cursos")
    for instancia in sesion.query(Curso).order_by(Curso.id_curso):
            print(instancia.id_curso, instancia.nombreCurso)
    while True:
        try:
            seleccion = int(input("Selecciona el numero del curso para ver el horario:"))
            numeroCurso = sesion.query(Curso).order_by(Curso.id_curso).count()
            if numeroCurso >= seleccion:
                for row in sesion.query(Curso).filter(Curso.id_curso == seleccion):
                    print()
                    print("El curso:", row.nombreCurso, "comienza a las ", row.horaCurso, ":00h")
                break

            elif numeroCurso < seleccion:
                print("opcion incorrecta")
                continue
        except ValueError:
            print("El valor seleccionado no es correcto")

def alumnosCurso():
    global sesion
    print("                         ")
    print("------  ALUMNOS DE UN CURSO ------------------")
    print("                         ")
    print("Estos son nuestros cursos")
    for instance in sesion.query(Curso).order_by(Curso.id_curso):
        print(instance.id_curso, instance.nombreCurso)
    while True:
        try:
            consAlum = int(input("seleccione el numero del curso para ver sus alumnos"))
            numeroCurso = sesion.query(Curso).order_by(Curso.id_curso).count()
            if consAlum <= numeroCurso :
                print("ALUMNOS:")
                numeroalumn=sesion.query(Alumnos).filter(Alumnos.cursoAlumno == consAlum).count()
                if numeroalumn > 0:
                    for row in sesion.query(Alumnos).filter(Alumnos.cursoAlumno == consAlum):
                        print(row.nombreAlumno, row.apellidoAlumno)
                else:
                    print("Este curso no tiene ningun alumno registrado")
                break
            else:
                print("opcion incorrecta")
                continue
        except ValueError:
            print("El valor seleccionado no es correcto")


def extraerdatos():
    select_profesor = select('*').select_from(Profesor)
    select_alumno   = select('*').select_from(Alumnos)
    select_curso    = select('*').select_from(Curso)
    select_horario  = select('*').select_from(Horario)
    res_prof        = sesion.execute(select_profesor).fetchall()
    res_al          = sesion.execute(select_alumno).fetchall()
    res_cur         = sesion.execute(select_curso).fetchall()
    res_hor         = sesion.execute(select_horario).fetchall()
    try:
        with open('data.csv', 'w') as filer:
            csv_out = csv.writer(filer)
            for fila in res_prof, res_al, res_cur, res_hor:
                csv_out.writerow(fila)
    except Exception as e:
        print (e)

def aplic():
    global sesion
    Base.metadata.create_all(engine)
    Session  = sessionmaker(bind=engine)
    sesion   = Session()
    prof1= Profesor(nombre_profesor='Profesor1', apellido_profesor='El 1',)
    prof2= Profesor(nombre_profesor='Profesor1', apellido_profesor='El 2',)
    prof3= Profesor(nombre_profesor='Profesor3', apellido_profesor='El 3')


    biologia = Curso(nombreCurso="Biologia",horaCurso=8)
    sesion.add(python)

    biologia.cursoProf.append(prof1)
    biologia.cursoProf.append(prof2)

    fisica = Curso(nombreCurso="Fisica",horaCurso=9)
    sesion.add(fisica)
    fisica.cursoProf.append(prof3)

    biologia.alumno =[Alumnos(nombreAlumno="Hugo",apellidoAlumno="Donald"),
               Alumnos(nombreAlumno="Paco",apellidoAlumno="Donald")]
    fisica.alumno=[Alumnos(nombreAlumno="Luis",apellidoAlumno="Donald"),
               Alumnos(nombreAlumno="Raton",apellidoAlumno="Perez")]
    sesion.commit()
    regist = mostrarMenu()

    while True:
        if regist==1:
            altaCurso()
            regist = mostrarMenu()
        elif regist==2:
            altaProfesor()
            regist = mostrarMenu()
        elif regist==3:
            altaAlumno()
            regist = mostrarMenu()
        elif regist==4:
            alumnosCurso()
            regist = mostrarMenu()
        elif regist==5:
            horarioProfesor()
            regist = mostrarMenu()
        elif regist==6:
            horarioCurso()
            regist = mostrarMenu()
        elif regist == 7:
            extraerdatos()
            regist = mostrarMenu()
        elif regist==8:
            print("Fin del prgrama")
            break

if __name__==__main__:
    aplic()