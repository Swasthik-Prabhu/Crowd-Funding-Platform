from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Campaign Model
class Campaign(Base):
    __tablename__ = 'campaigns'

    camp_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    cause = Column(String, nullable=False)
    target_amount = Column(Float, nullable=False)
    raised_amount = Column(Float, default=0.0)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    # Foreign key for the creator (linked to Users table)
    creator_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    # Relationships
    creator = relationship("Users", back_populates="campaigns")
    milestones = relationship("MileStone", back_populates="campaign")
    reports = relationship("Report", back_populates="campaign")
    donations = relationship("Donations", back_populates="campaign")  # Added donations relationship
    beneficiaries = relationship("Beneficiaries", back_populates="campaign")  # Added relationship

# Beneficiaries Model
class Beneficiaries(Base):
    __tablename__ = 'beneficiaries'

    beneficiary_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact = Column(Integer, nullable=False, unique=True)
    address = Column(String, nullable=False)
    

    campaign_id = Column(Integer, ForeignKey('campaigns.camp_id'), nullable=False)

    # Relationships
    campaign = relationship("Campaign", back_populates="beneficiaries")

# Donations Model
class Donations(Base):
    __tablename__ = 'donations'

    donation_id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    donation_date = Column(DateTime, nullable=False)
    transaction_id = Column(Integer, nullable=False, unique=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.camp_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)  # Foreign key for User

    # Relationship with Campaign
    campaign = relationship("Campaign", back_populates="donations")

    # Relationship with User
    user = relationship("Users", back_populates="donations")


# Users Model
class Users(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact = Column(Integer, nullable=False, unique=True)
    role = Column(String, nullable=False)
    email = Column(String ,nullable = False)
    password = Column(String, nullable = False)

    # Relationship with Campaign and Report
    campaigns = relationship("Campaign", back_populates="creator")  # Added campaigns relationship
    reports = relationship("Report", back_populates="user")
    donations = relationship("Donations", back_populates="user")  # Added donations relationship

# Report Model
class Report(Base):
    __tablename__ = 'reports'

    report_id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.camp_id'), nullable=False)
    report_date = Column(DateTime, nullable=False)
    description = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    # Relationships
    campaign = relationship("Campaign", back_populates="reports")
    user = relationship("Users", back_populates="reports")

# Milestone Model
class MileStone(Base):
    __tablename__ = 'milestones'

    milestone_id = Column(Integer, primary_key=True, index=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.camp_id'), nullable=False)
    milestone_date = Column(DateTime, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, nullable=False)

    # Relationship with Campaign
    campaign = relationship("Campaign", back_populates="milestones")
