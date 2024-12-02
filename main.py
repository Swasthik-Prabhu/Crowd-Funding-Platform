from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import schemas
from database import engine, Sessionlocal
from models import Base, Campaign, Beneficiaries, Donations, Users, Report, MileStone
from schemas import Campaign as CampaignSchema, Beneficiaries as BeneficiariesSchema, Donations as DonationsSchema, Users as UsersSchema, Report as ReportSchema, MileStone as MileStoneSchema
# from passlib.context import CryptContext


from hashing import Hash


# Initialize FastAPI app
app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Dependency for getting DB session
def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()

# Campaign Endpoints
@app.post("/campaigns/", response_model=CampaignSchema,tags=['Campaign'])
def create_campaign(campaign: CampaignSchema, db: Session = Depends(get_db)):
    db_campaign = Campaign(
        title=campaign.title,
        cause=campaign.cause,
        target_amount=campaign.target_amount,
        raised_amount=campaign.raised_amount,
        start_date=campaign.start_date,
        end_date=campaign.end_date,
        creator_id=campaign.creator_id  # This links to the Users table
    )
    db.add(db_campaign)
    db.commit()
    db.refresh(db_campaign)
    return db_campaign


@app.get("/campaigns/{campaign_id}", response_model=CampaignSchema,tags=['Campaign'])
def get_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.camp_id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@app.put("/campaigns/{campaign_id}", response_model=CampaignSchema,tags=['Campaign'])
def update_campaign(campaign_id: int, updated_campaign: CampaignSchema, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.camp_id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    for key, value in updated_campaign.dict(exclude_unset=True).items():
        setattr(campaign, key, value)
    
    db.commit()
    db.refresh(campaign)
    return campaign



@app.delete("/campaigns/{campaign_id}", tags=['Campaign'])
def delete_campaign(campaign_id: int, db: Session = Depends(get_db)):
    campaign = db.query(Campaign).filter(Campaign.camp_id == campaign_id).first()
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    db.delete(campaign)
    db.commit()
    return {"detail": "Campaign deleted successfully"}




# Beneficiary Endpoints
@app.post("/beneficiaries/", response_model=BeneficiariesSchema,tags=['Beneficiary'])
def create_beneficiary(beneficiary: BeneficiariesSchema, db: Session = Depends(get_db)):
    db_beneficiary = Beneficiaries(**beneficiary.dict())
    db.add(db_beneficiary)
    db.commit()
    db.refresh(db_beneficiary)
    return db_beneficiary

@app.get("/beneficiaries/{beneficiary_id}/", response_model=BeneficiariesSchema,tags=['Beneficiary'])
def get_beneficiary(beneficiary_id: int, db: Session = Depends(get_db)):
    beneficiary = db.query(Beneficiaries).filter(Beneficiaries.beneficiary_id == beneficiary_id).first()
    if not beneficiary:
        raise HTTPException(status_code=404, detail="Beneficiary not found")
    return beneficiary

@app.put("/beneficiaries/{beneficiary_id}", response_model=BeneficiariesSchema,tags=['Beneficiary'])
def update_beneficiary(beneficiary_id: int, updated_beneficiary: BeneficiariesSchema, db: Session = Depends(get_db)):
    beneficiary = db.query(Beneficiaries).filter(Beneficiaries.beneficiary_id == beneficiary_id).first()
    if not beneficiary:
        raise HTTPException(status_code=404, detail="Beneficiary not found")

    for key, value in updated_beneficiary.dict(exclude_unset=True).items():
        setattr(beneficiary, key, value)
    
    db.commit()
    db.refresh(beneficiary)
    return beneficiary



@app.delete("/beneficiaries/{beneficiary_id}", tags=['Beneficiary'])
def delete_beneficiary(beneficiary_id: int, db: Session = Depends(get_db)):
    beneficiary = db.query(Beneficiaries).filter(Beneficiaries.beneficiary_id == beneficiary_id).first()
    if not beneficiary:
        raise HTTPException(status_code=404, detail="Beneficiary not found")
    db.delete(beneficiary)
    db.commit()
    return {"detail": "Beneficiary deleted successfully"}



# Donations Endpoints
@app.post("/donations/", response_model=DonationsSchema,tags=['Donations'])
def create_donation(donation: DonationsSchema, db: Session = Depends(get_db)):
    # Check if user exists
    db_user = db.query(Users).filter(Users.user_id == donation.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_donation = Donations(
        amount=donation.amount,
        donation_date=donation.donation_date,
        transaction_id=donation.transaction_id,
        campaign_id=donation.campaign_id,
        user_id=donation.user_id
    )
    db.add(db_donation)
    db.commit()
    db.refresh(db_donation)
    return db_donation


@app.get("/donations/{donation_id}/", response_model=DonationsSchema,tags=['Donations'])
def get_donation(donation_id: int, db: Session = Depends(get_db)):
    donation = db.query(Donations).filter(Donations.donation_id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    return donation


@app.put("/donations/{donation_id}", response_model=DonationsSchema,tags=['Donations'])
def update_donation(donation_id: int, updated_donation: DonationsSchema, db: Session = Depends(get_db)):
    donation = db.query(Donations).filter(Donations.donation_id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")

    for key, value in updated_donation.dict(exclude_unset=True).items():
        setattr(donation, key, value)
    
    db.commit()
    db.refresh(donation)
    return donation


@app.delete("/donations/{donation_id}", tags=['Donations'])
def delete_donation(donation_id: int, db: Session = Depends(get_db)):
    donation = db.query(Donations).filter(Donations.donation_id == donation_id).first()
    if not donation:
        raise HTTPException(status_code=404, detail="Donation not found")
    db.delete(donation)
    db.commit()
    return {"detail": "Donation deleted successfully"}




# Users Endpoints
@app.post("/users/", response_model=UsersSchema,tags=['Users'])
def create_user(user: UsersSchema, db: Session = Depends(get_db)):
    # Check if email or contact already exists
    db_user_email = db.query(Users).filter(Users.email == user.email).first()
    db_user_contact = db.query(Users).filter(Users.contact == user.contact).first()
    if db_user_email:
        raise HTTPException(status_code=400, detail="Email already registered")
    if db_user_contact:
        raise HTTPException(status_code=400, detail="Contact already registered")
    
    hashedPassword = Hash.bcrypt(password = user.password)
    db_user = Users(
        name=user.name,
        email=user.email,
        password=hashedPassword,
        contact=user.contact,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@app.get("/users/{user_id}/", response_model=schemas.ShowUser,tags=['Users'])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UsersSchema,tags=['Users'])
def update_user(user_id: int, updated_user: UsersSchema, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in updated_user.dict(exclude_unset=True).items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user



@app.delete("/users/{user_id}", tags=['Users'])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(Users).filter(Users.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}


# Reports Endpoints
@app.post("/reports/", response_model=ReportSchema,tags=['Reports'])
def create_report(report: ReportSchema, db: Session = Depends(get_db)):
    db_report = Report(**report.dict())
    db.add(db_report)
    db.commit()
    db.refresh(db_report)
    return db_report

@app.get("/reports/{report_id}/", response_model=ReportSchema,tags=['Reports'])
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.report_id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

@app.put("/reports/{report_id}", response_model=ReportSchema,tags=['Reports'])
def update_report(report_id: int, updated_report: ReportSchema, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.report_id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")

    for key, value in updated_report.dict(exclude_unset=True).items():
        setattr(report, key, value)
    
    db.commit()
    db.refresh(report)
    return report




@app.delete("/reports/{report_id}", tags=['Reports'])
def delete_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(Report).filter(Report.report_id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    db.delete(report)
    db.commit()
    return {"detail": "Report deleted successfully"}


# Milestone Endpoints
@app.post("/milestones/", response_model=MileStoneSchema,tags=['Milestone'])
def create_milestone(milestone: MileStoneSchema, db: Session = Depends(get_db)):
    db_milestone = MileStone(**milestone.dict())
    db.add(db_milestone)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone

@app.get("/milestones/{milestone_id}/", response_model=MileStoneSchema,tags=['Milestone'])
def get_milestone(milestone_id: int, db: Session = Depends(get_db)):
    milestone = db.query(MileStone).filter(MileStone.milestone_id == milestone_id).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    return milestone

@app.put("/milestones/{milestone_id}", response_model=MileStoneSchema,tags=['Milestone'])
def update_milestone(milestone_id: int, updated_milestone: MileStoneSchema, db: Session = Depends(get_db)):
    milestone = db.query(MileStone).filter(MileStone.milestone_id == milestone_id).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")

    for key, value in updated_milestone.dict(exclude_unset=True).items():
        setattr(milestone, key, value)
    
    db.commit()
    db.refresh(milestone)
    return milestone



@app.delete("/milestones/{milestone_id}", tags=['Milestone'])
def delete_milestone(milestone_id: int, db: Session = Depends(get_db)):
    milestone = db.query(MileStone).filter(MileStone.milestone_id == milestone_id).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    db.delete(milestone)
    db.commit()
    return {"detail": "Milestone deleted successfully"}