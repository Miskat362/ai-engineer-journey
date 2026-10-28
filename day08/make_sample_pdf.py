from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak

styles = getSampleStyleSheet()

sections = [
    ("1. Working Hours",
     "Our office hours are Sunday to Thursday, 9 AM to 6 PM. Employees may start between "
     "8 AM and 10 AM as long as they complete 8 working hours that day. Friday and Saturday "
     "are weekly holidays. Overtime must be approved by the line manager in advance, and "
     "approved overtime is compensated with time off in lieu within the same month."),
    ("2. Annual Leave",
     "Full-time employees receive 20 days of paid annual leave per calendar year. Up to 5 "
     "unused days may be carried over to the next year; any additional unused days expire "
     "on December 31. Leave requests longer than 3 consecutive days must be submitted at "
     "least 14 days in advance through the HR portal. New employees accrue leave monthly "
     "during their first year."),
    ("3. Sick Leave",
     "Employees receive 10 days of paid sick leave per year. A medical certificate is "
     "required for any absence longer than 2 consecutive days. Sick leave does not carry "
     "over to the next year. Employees should notify their manager before 10 AM on the "
     "first day of absence."),
    ("4. Remote Work",
     "Employees may work remotely up to 3 days per week with line manager approval. "
     "Employees in their first 3 months (probation period) must work from the office. "
     "Remote workers must be reachable on Slack during core hours, 11 AM to 4 PM. "
     "Requests for more than 3 remote days per week need written approval from the "
     "department head."),
    ("5. Expense Reimbursement",
     "Expenses under $50 need only a receipt photo. Expenses between $50 and $500 need "
     "manager approval before the purchase. Expenses above $500 need department head "
     "approval. All claims must be submitted within 30 days of the purchase and are "
     "reimbursed on the 5th of the following month."),
    ("6. Company Equipment",
     "The company provides a laptop to every full-time employee. Equipment must be "
     "returned within 7 days of the last working day. Lost or stolen equipment must be "
     "reported to the IT team within 24 hours. Personal use of company laptops is "
     "permitted but must not violate the IT security policy."),
]

doc = SimpleDocTemplate("company_policy.pdf", pagesize=A4)
story = [Paragraph("TechCorp Employee Handbook", styles["Title"]), Spacer(1, 20)]

for i, (heading, body) in enumerate(sections):
    story.append(Paragraph(heading, styles["Heading2"]))
    story.append(Paragraph(body, styles["BodyText"]))
    story.append(Spacer(1, 16))
    if i == 2:                     # adding page break to make more page in pdf
        story.append(PageBreak())

doc.build(story)
print("company_policy.pdf created")