from flask import Flask,render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import date
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_BINDS'] = {
    'amount': 'sqlite:///amount.db',
    'goals' : 'sqlite:///goals.db',
    'months':'sqlite:///months.db',
    'all_record':'sqlite:///all_record.db'

}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Money(db.Model):
    today = date.today()


    d1 = today.strftime(r"%d/%m/%Y")
    sno = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(12), default=d1)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.amount}"
class Budget(db.Model): 
    __bind_key__ = 'amount'
    __tablename__ = 'budget'
    id = db.Column(db.Integer, primary_key=True)
    budget = db.Column(db.Integer)
    def __repr__(self) -> str:
        return f"{self.id} - {self.budget}"

class Goals(db.Model):
    __bind_key__ = 'goals'
    sno = db.Column(db.Integer, primary_key=True)
    Amount = db.Column(db.Integer)
    desc = db.Column(db.String(500))
    msg = db.Column(db.String(5000))
    def __repr__(self) -> str:
        return f"{self.sno} - {self.Amount} - {self.desc}"
class months(db.Model):
    __bind_key__ = 'months'
    sno = db.Column(db.Integer,primary_key=True)
    Budget = db.Column(db.Integer,nullable=True)
    expenses= db.Column(db.Integer,nullable=True)
class all_record(db.Model):
    __bind_key__ = 'all_record'
    sno = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(500), nullable=False)
    date = db.Column(db.String(12), nullable=False)


# Variales to WOrk with 

@app.route("/", methods=['GET', 'POST'])
def hello():
    if request.method == 'POST':
        amount = request.form['amount']
        reason = request.form['reason']
        date = request.form['date']
        from datetime import datetime

# Assuming you have a date string in the format yyyy-mm-dd
        input_date_string = date

        # Convert the input string to a datetime object
        input_date = datetime.strptime(input_date_string, "%Y-%m-%d")

        # Format the date as dd/mm/yyyy
        formatted_date = input_date.strftime("%d/%m/%Y")
        if amount != '' and reason != '':
            money = Money(amount=amount, reason=reason , date=formatted_date)
            db.session.add(money)
            db.session.commit()
    allmoney = Money.query.order_by(Money.date).all()
    sum = 0

    date_1 = 0
    if len(allmoney) != 0:
        date_last = int(allmoney[len(allmoney)-1].date[:2])
        
     # days_till_now = date_last - date_1
    else :        
        date_last = 30
        days_till_now = 30
    if len(allmoney)<1 :
        month_1 = False
        month_2 = False
       
    else:
         month_1 = int(allmoney[0].date[3:5])
         month_2 = int(allmoney[len(allmoney)-1].date[3:5])
    for i in allmoney:
        if i.amount:
         sum = sum + int(i.amount)
    dates = set()
    dates_list = list()
   
    for i in allmoney:
        dates.add(i.date)
        dates_list.append(i.date)
    avg = 0
    if len(dates)!=0:
        avg = f"{(sum)/(date_last):.0f}"
    main_amount = 1345
    budget =Budget.query.filter_by(id=1).first()
    main_amount = budget.budget
    expenses_per_day = list()
    expenses_each = 0

    for i in dates:
        for m in allmoney:
            if i == m.date:
                    if m.amount:
                         expenses_each += int(m.amount)
        expenses_per_day.append(expenses_each)
        expenses_each = 0
    labels = list(dates)
    data = expenses_per_day
    try :
        n_Avg = f'{(budget.budget - sum) / (30 -date_last):.0f}'
    
    except:
        n_Avg = 0
    
    print(f"month 1 and 3 are {month_1},{month_2}")
    allgoals = Goals.query.all()
    if month_1 != month_2:
        for i in allmoney[:(len(allmoney)-2)]:
            trecord = all_record(amount=i.amount, reason=i.reason , date=i.date)
            db.session.add(trecord)
            db.session.commit()
            money = Money.query.filter_by(sno=i.sno).first()
            if money:
                db.session.delete(money)
                db.session.commit()
            else:
            # Log or handle the case where money is not found
                print(f"Money with sno={i.sno} not found.")
        # days_till_now = 30
    
    
    return render_template("index.html", money=allmoney,sum=sum,avg=avg,dates=dates,main_amount=main_amount,goals=allgoals,n_Avg=n_Avg,days_till_now=date_last,dates_list=dates_list,data=data,
    labels=labels)
@app.route("/delete/<int:sno>")
def delete(sno):
    money = Money.query.filter_by(sno=sno).first()
    if money:
            db.session.delete(money)
            db.session.commit()
    else:
            # Log or handle the case where money is not found
            print(f"Money not found.")
    print("deleted")
    return redirect("/")
@app.route("/delete_goals/<int:sno>")
def delete_goals(sno):
    money = Goals.query.filter_by(sno=sno).first()
    db.session.delete(money)
    db.session.commit()
    print("deleted")
    return redirect("/")
@app.route("/all_record")
def all_rec():
    all_records = all_record.query.all()
    # for i in all_records:
    #     if i.amount:
    #         sum = sum + int(i.amount)
    return render_template('all_record.html',money=all_records,)
@app.route("/edit/<int:sno>", methods=['GET', 'POST'])
def edit(sno):
     if request.method =='POST':
        amount = request.form['amount']
        reason = request.form['reason']
        if amount != '' and reason != '':
            amoney = Money.query.filter_by(sno=sno).first()
            amoney.amount = amount
            amoney.reason = reason
            db.session.add(amoney)
            db.session.commit()
            return redirect("/")
     amoney = Money.query.filter_by(sno=sno).first()
     return render_template('edit.html',money=amoney)
@app.route("/edit_goals/<int:sno>", methods=['GET', 'POST'])
def edit_goals(sno):
     if request.method =='POST':
        amount = request.form['amount']
        desc = request.form['cause']
        if amount != '' and desc != '':
            amoney = Goals.query.filter_by(sno=sno).first()
            amoney.Amount = amount
            amoney.desc = desc
            db.session.add(amoney)
            db.session.commit()
            return redirect("/")
     amoney = Goals.query.filter_by(sno=sno).first()
     return render_template('edit_goals.html',edited=amoney)


@app.route("/edit_a", methods=['GET', 'POST'])
def edit_amount():
    main_amount = Budget.query.get(1)  # Assuming you have only one record with id=1
    if request.method == 'POST':
        new_amount = request.form['new_amount']
        main_amount.budget = new_amount  # Update the 'budget' attribute
        db.session.commit()
        return redirect("/")
    return render_template('edit_a.html', main_amount=main_amount)
@app.route("/goal", methods=['GET', 'POST'])
def goal():
    if request.method == 'POST':
        Amount = request.form['amount']
        cause = request.form['cause']
        budget =Budget.query.filter_by(id=1).first()
        allmoney = Money.query.all()
        sum = 0

        date_1 = 0
        import datetime

        x = datetime.datetime.now().strftime("%d")

        for i in allmoney:
          if i.amount:
             sum = sum + int(i.amount)
        dates = set()
        for i in allmoney:
            dates.add(i.date)
        r_amount = (budget.budget-sum)
        msg =""
        if int(Amount) <= r_amount:
            r_avg = (r_amount -int(Amount)) / (30 -int(x))
            msg = "You can complete this goal but then you have to complete remaining month with Avg of Rs. "+f'{r_avg:.0f}'
        
        else:
            msg = "You can't complete this goal now as your budget is Rs. "+f'{r_amount:.0f}'
        if Amount != '' and cause != '':
            goal = Goals(Amount=Amount, desc=cause,msg=msg)
            db.session.add(goal)
            db.session.commit()
            return redirect("/")
    allgoals = Goals.query.order_by(Goals.sno).all()
    print(allgoals)
    return render_template("/", goals=allgoals)
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Create the tables
    app.run(debug=True)