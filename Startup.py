# Copyright 2017 Keegan Joseph Brophy
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
from flask import *
from werkzeug.utils import *

from orginization_functions import *

reload(sys)
sys.setdefaultencoding('utf-8')


app = Flask(__name__)
DATABASE = 'database.db'
db = SqliteDatabase(DATABASE)
UPLOAD_FOLDER = ''
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
	return '.' in filename and \
		   filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/export', methods=['GET','POST'])
def docustomexport():
	if request.method == 'POST':
		selector = request.form.get('Select')
		export_file(selector)
		name = selector+'.csv'
		return send_file(name,mimetype=None,as_attachment=True)
	return render_template('export.html')


@app.route('/import', methods=['GET', 'POST'])
def docustomimport():
	if request.method == 'POST':
		selector = request.form.get('Select')
		import_file(selector)
	return render_template('import.html')


@app.route('/favicon.ico')
def favicon():
	return send_from_directory(os.path.join(app.root_path, 'static'),
							   'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/splits')
def splits():
	start_splitting()
	return redirect('/listm')

@app.route('/offering')
def offergen():
	# ######################semester_quick_gen(fromD)
	semester_quick_gen(2008)
	# #####################person(name,email)
	person('Mr. Anderson','jonathan.anderson@mun.ca',2012,3)
	person('Mr. Anders54on','jon56athan.anderson@mun.ca',2008,3)
	person('Mr. Anon','jonathan.arson@mun.ca',2013,3)
	lang(2015)
	lazy_lang(2015)
	# ################student(name, email)
	student('Juteau','2011205085')
	student('Derakhshan Nik','201509962')
	student('Nguyen','201051471')
	# ##################superC(BOOLDoyouwanttocreateanewone,Description,Weight)
	superC(False,'lol',400)
	# #############supera(TermS,profid,Studentid,supervisoncalss,session)
	supera(2015,1,1,1,1)
	supera(2015,2,1,1,1)
	supera(2015,1,2,1,2)
	supera(2015,1,1,1,3)
	supera(2015,2,1,1,3)
	supera(2015,1,2,1,3)
	supera(2015,2,2,1,3)
	supera(2015,1,3,1,3)
	# ###########offer(year,code,session,profid,numberofstudents,sectionnumbers):
	offer(2015,1020,2,1,80,3)
	offer(2015,1020,2,3,80,3)
	offer(2015,3891,1,1,80,1)
	offer(2015,8894,2,1,70,1)
	offer(2015,8894,2,3,70,1)
	offer(2015,3891,1,2,80,1)
	offer(2015,8894,2,2,70,1)
	person1=Person.select()
	for ixd in person1:
		update=Mastermany.update(split=1).where(Mastermany.instructor == ixd.id)
		update.execute()
	return redirect('/listm')


@app.route("/course/<id>", methods=['GET', 'POST'])
def Coursehist(id):
	list2=[]
	course = Course.get(Course.id==id)
	generation = (CourseGeneration.select().join(Course).where(Course.id == id))
	list1=informationXchange(generation,list2)
	return render_template("course.html", course=course,generation=generation,list1=list1)


@app.route("/c/<id>", methods=['GET', 'POST'])
def Courseh(id):
	list2=[]
	course = Course.get(Course.code==id)
	generation = (CourseGeneration.select().join(Course).where(Course.code == id))
	list1=informationXchange(generation,list2)
	return render_template("course.html", course=course,generation=generation,list1=list1)


@app.route("/gen/<id>", methods=['GET', 'POST'])
def gen(id):
	list2=[]
	gen=CourseGeneration.get(CourseGeneration.id == id)
	course = Course.get(Course.code == gen.course.code)
	generation = (CourseGeneration.select().join(Course).where(Course.code == gen.course.code))
	list1=informationXchange(generation,list2)
	return render_template("course.html", course=course,generation=generation,list1=list1)


@app.route("/profile/<prof_id>/history", methods=['GET', 'POST'])
def Profilehist(prof_id):
	person = Person.get(Person.id == prof_id)
	supervision = (Supervision
				   .select()
				   .join(Mastermany)
				   .where(Mastermany.instructor == prof_id)
				   .order_by(Supervision.semester.desc()))
	projectsupervision = (ProjectSupervision
						  .select()
						  .join(Mastermany)
						  .where(Mastermany.instructor == prof_id)
						  .order_by(ProjectSupervision.semester.desc()))
	offering = (Mastermany
				.select()
				.join(Offering)
				.where(Mastermany.instructor == prof_id)
				.order_by(Offering.semester.desc()))
	adjustment = (Adjustment
				  .select()
				  .join(Person)
				  .where(Person.id == prof_id)
				  .order_by(Adjustment.id.desc()))
	mastermany=Mastermany.select().where(Mastermany.instructor==prof_id)
	Stotal = 0
	Atotal = 0
	Ptotal = 0
	Ototal = 0
	Snum = (Supervision
				  .select()
				  .join(Mastermany)
				  .where(Mastermany.instructor == prof_id))
	for num in Snum:
		Ssum=Mastermany.select().where(Mastermany.sid==num.id).get()
		Stotal+=num.supervision_class_id.weight*Ssum.split

	Onum = (Offering
				  .select()
				  .join(Mastermany)
				  .where(Mastermany.instructor == prof_id))
	for num in Onum:
		Osum=Mastermany.select().where(Mastermany.oid==num.id).get()
		print num.weight
		print Osum.split
		Ototal+=num.weight*Osum.split

	# Ptotal = (ProjectSupervision
	# 			  .select()
	# 			  .where(ProjectSupervision.prof_id == prof_id)
	# 			  .join(ProjectClass)
	# 			  .select(fn.SUM(ProjectClass.weight)))
	# Stotal=sup_totals(prof_id)
	# Ototal=off_totals(prof_id)
	# Ptotal=pro_totals(prof_id)
	Atotal = (Person
			  .select()
			  .where(Person.id == prof_id)
			  .join(Adjustment)
			  .select(fn.SUM(Adjustment.weight))
			  .scalar())
	defi=deficit(prof_id)
	if Ototal is None:
		Ototal = 0
	if Atotal is None:
		Atotal = 0
	if Stotal is None:
		Stotal = 0
	if Ptotal is None:
		Ptotal = 0
	total = (Ptotal) + (Atotal) + (Stotal) + (Ototal) - defi
	if request.method == 'POST':
		if request.form['subm1'] == "submit2":
			# semesterID1 = request.form['SemesterID1']
			# student = request.form['stu']
			# iD1 = request.form['ID1']
			# courseGenID = request.form['CourseGenID']
			weight = request.form['weight']
			myid = request.form['myid']
			update=Offering.update(weight=weight).where(Offering.id==myid)
			update.execute()
	return render_template("profilehist.html", person=person, supervision=supervision,instructor=prof_id,
						   projectsupervision=projectsupervision, offering=offering, adjustment=adjustment,total=total,
						   Stotal=Stotal,Ototal=Ototal,Onum=Onum,deficit=defi)


@app.route("/profile/<prof_id>", methods=['GET', 'POST'])
def Profile(prof_id):
	now = datetime.datetime.now()
	year1 = now.year
	person = Person.get(Person.id == prof_id)
	supervision = (Supervision.select()
				   .join(Person, on=(Supervision.id == Person.id))
				   .join(Term, on=(Supervision.id == Term.id))
				   .where(Person.id == prof_id, Term.year == year1)
				   .order_by(Supervision.id.desc()))
	projectsupervision = (ProjectSupervision
						  .select()
						  .join(Person, on=(ProjectSupervision.id == Person.id))
						  .join(Term, on=(ProjectSupervision.id == Term.id))
						  .where(Person.id == prof_id, Term.year == year1)
						  .order_by(ProjectSupervision.id.desc()))
	offering = (Offering
				.select()
				.join(Mastermany, on=(Offering.id == Mastermany.instructor))
				.join(Term, on=(Offering.id == Term.id))
				.where(Mastermany.id == prof_id, Term.year == year1)
				.order_by(Offering.id.desc()))
	adjustment = (Adjustment
				  .select()
				  .join(Person)
				  .where(Person.id == prof_id)
				  .order_by(Adjustment.id.desc()))
	Stotal = 0
	Atotal = 0
	Ptotal = 0
	Ototal = 0
	Stotal = (Supervision
			  .select()
			  .where(Supervision.instructor == prof_id)
			  .join(SupervisionClass)
			  .select(fn.SUM(SupervisionClass.weight))
			  .scalar())
	Atotal = (Person
			  .select()
			  .where(Person.id == prof_id)
			  .join(Adjustment)
			  .select(fn.SUM(Adjustment.weight))
			  .scalar())
	Ototal = (Offering
			  .select()
			  .join(Mastermany)
			  .where(Mastermany.instructor == prof_id)
			  .select(fn.SUM(Offering.weight))
			  .scalar())
	Ptotal = (ProjectSupervision
			  .select()
			  .where(ProjectSupervision.instructor == prof_id)
			  .join(ProjectClass)
			  .select(fn.SUM(ProjectClass.weight))
			  .scalar())
	defi = deficit(prof_id)
	if Atotal is None:
		Atotal = 0
	if Stotal is None:
		Stotal = 0
	if Ptotal is None:
		Ptotal = 0
	total = (Ptotal) + (Atotal) + (Stotal) + (Ototal) - (defi)
	if request.method == 'POST':
		if request.form['subm1'] == "submit2":
			# semesterID1 = request.form['SemesterID1']
			# student = request.form['stu']
			# iD1 = request.form['ID1']
			# courseGenID = request.form['CourseGenID']
			weight = request.form['weight']
			myid = request.form['myid']
			update = Offering.update(weight=weight).where(Offering.id == myid)
			update.execute()
	return render_template("profilehist.html", person=person, supervision=supervision, instructor=prof_id,
						   projectsupervision=projectsupervision, offering=offering, adjustment=adjustment, total=total,
						   Stotal=Stotal, Ototal=Ototal)


@app.route('/listm', methods=['GET', 'POST'])
def listm():
	if request.method == 'POST':
		if request.form['subm1'] == "submit1":
			labs = request.form['Labs']
			credit = request.form['Credit']
			title = request.form['Title']
			cRN = request.form['CRN']
			CourseGeneration.create(labs=labs, credit_hours=credit, title=title, course=cRN)
		elif request.form['subm1'] == "submit2":
			semesterID1 = request.form['SemesterID1']
			student = request.form['stu']
			iD1 = request.form['ID1']
			courseGenID = request.form['CourseGenID']
			Offering.create(enrolment=student, instructor=iD1, semester=semesterID1, generation=courseGenID)
		elif request.form['subm1'] == "submit3":
			sID = request.form['StudentID']
			superclass = request.form['SupervisionClassID']
			semesterID2 = request.form['SemesterID2']
			iD2 = request.form['ID2']
			Supervision.create(instructor=iD2, student_id=sID, supervision_class_id=superclass, semester=semesterID2)
		elif request.form['subm1'] == "submit4":
			iD3 = request.form['ID3']
			semesterID3 = request.form['SemesterID3']
			pseudoID = request.form['PseudoID']
			projectClassID = request.form['ProjectClassID']
			ProjectSupervision.create(instructor=iD3, Team=pseudoID, project_class_id=projectClassID,
									  semester=semesterID3)
		elif request.form['subm1'] == "submit5":
			iD4 = request.form['ID4']
			ADJWeight = request.form['ADJWeight']
			AUDITCOMMENT = request.form['AUDITCOMMENT']
			Adjustment.create(instructor=iD4, weight=ADJWeight, audit_comment=AUDITCOMMENT)
	mastermany = Mastermany.select().order_by(Mastermany.oid.asc())
	return render_template("masterlist.html", Person=Person, ProjectType=ProjectType, Course=Course,
						   SupervisionClass=SupervisionClass, ProjectClass=ProjectClass,
						   ProjectSupervision=ProjectSupervision, Supervision=Supervision, Adjustment=Adjustment,
						   Role=Role, Term=Term, Offering=Offering,
						   CourseGeneration=CourseGeneration, Student=Student,Mastermany=mastermany)


@app.route('/Dashboard')
@app.route('/index')
@app.route('/', methods=["GET"])
def index():
	return render_template("home.html")


@app.route('/peeweetable', methods=["GET", "POST"])
def peeweetable():
	if request.method == 'POST':
		if request.form['Full'] == 'Drop and ReCreate':
			db.connect()
			# removed Course and CourseGeneration
			db.drop_tables(
				[Person,Mastermany,
				 # Term,
				 Offering,
				 # Course,
				 Role, ProjectSupervision, ProjectClass,
				 Supervision,
				 # CourseGeneration,
				 SupervisionClass, ProjectType,
				 Student, Adjustment],safe=True)
			db.create_tables(
				[Person,Mastermany,
				 # Term,
				 Offering,
				 # Course,
				 Role, ProjectSupervision, ProjectClass,
				 Supervision,
				 # CourseGeneration,
					SupervisionClass, ProjectType, Student, Adjustment],safe=True)
			db.close()
		elif request.form['Full'] == 'Create':
			db.connect()
			db.create_tables(
				[Person, Mastermany,
				 # Term,
				 Offering,
				 # Course,
					Role, ProjectSupervision, ProjectClass,
				 Supervision,
				 # CourseGeneration,
				 SupervisionClass, ProjectType, Student, Adjustment],safe=True)
			db.close()
		elif request.form['Full'] == 'Drop':
			db.connect()
			db.drop_tables(
				[Person, Mastermany,
				 # Term,
				 Offering,
				 # Course,
				 Role, ProjectSupervision, ProjectClass,
				 Supervision,
				 # CourseGeneration,
				 SupervisionClass, ProjectType, Student, Adjustment],safe=True)
			db.close()
	return render_template('reset.html')


if __name__ == '__main__':
	app.config["SECRET_KEY"] = "Ravioli"
app.run(port=5000, debug=True)
