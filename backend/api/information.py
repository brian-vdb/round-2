# api/information.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class InfoItem(BaseModel):
  question: str
  answer: str

# Placeholder entries regarding innovation aligned with TCS Pace Port themes
INFORMATION: List[InfoItem] = [
  {"question": "What is the TCS Pace Port?", "answer": "TCS Pace Port is an open innovation ecosystem that connects startups, enterprises, and academic institutions to co-create and pilot new technologies at scale."},
  {"question": "How does Pace Port support digital transformation?", "answer": "By providing access to cutting-edge labs, design thinking workshops, and a network of industry experts, Pace Port accelerates digital transformation journeys for clients across sectors."},
  {"question": "What industries does Pace Port focus on?", "answer": "Pace Port focuses on a broad range of industries including banking, retail, manufacturing, healthcare, and telecommunications to drive industry-specific innovation."},
  {"question": "How can enterprises collaborate with startups at Pace Port?", "answer": "Enterprises can join co-innovation programs, attend demo days, and leverage sandbox environments to pilot startup solutions in real-world scenarios."},
  {"question": "What are the key drivers of innovation at Pace Port?", "answer": "The key drivers include customer-centric design, agile development, data-driven insights, and strategic partnerships with technology leaders."},
  {"question": "What is the role of design thinking at Pace Port?", "answer": "Design thinking workshops at Pace Port help cross-functional teams empathize with users, ideate solutions, and prototype concepts rapidly to validate value propositions."},
  {"question": "How does Pace Port measure success?", "answer": "Success is measured by the number of proof-of-concepts deployed, time-to-market reduction, ROI from pilot projects, and client satisfaction scores."},
  {"question": "What labs are available at Pace Port locations?", "answer": "Labs include IoT & Edge Computing Lab, AI & Machine Learning Lab, Blockchain & Distributed Ledger Lab, and Cloud Innovation Lab."},
  {"question": "How does Pace Port integrate with existing IT landscapes?", "answer": "Pace Port uses API-led integration, microservices architecture, and secure gateways to seamlessly connect new innovations with legacy systems."},
  {"question": "Can academic researchers access Pace Port resources?", "answer": "Yes, academic researchers can partner through university programs, access lab facilities, and contribute to joint publications and patent filings."},
  {"question": "What type of funding support is available for startups at Pace Port?", "answer": "Selected startups may receive seed funding, co-investment opportunities, and access to TCS venture capital networks based on pilot outcomes."},
  {"question": "How are intellectual property rights managed?", "answer": "IP agreements are tailored to each engagement, ensuring clear ownership, licensing terms, and revenue-sharing models for co-created solutions."},
  {"question": "What is the typical engagement model?", "answer": "Engagements range from short-term hackathons to long-term co-innovation projects, usually structured as workshops, sprints, or incubation programs."},
  {"question": "How does Pace Port foster a culture of continuous innovation?", "answer": "Through regular innovation challenges, hackathons, speaker series, and an internal intrapreneurship platform that recognizes and rewards new ideas."},
  {"question": "What is the onboarding process for new collaborators?", "answer": "New collaborators go through an orientation session, access setup, NDA execution, and an initial project scoping workshop within the first week."},
  {"question": "How does data security work in Pace Port projects?", "answer": "Data security is enforced via end-to-end encryption, role-based access controls, and compliance with ISO 27001 and GDPR standards."},
  {"question": "Can clients customize the Pace Port framework?", "answer": "Yes, the framework is modular and can be tailored to specific business objectives, technology stacks, and governance models per client needs."},
  {"question": "What success stories have emerged from Pace Port?", "answer": "Previous pilots include AI-driven predictive maintenance in manufacturing, blockchain-based trade finance platforms, and AR-enabled retail experiences that led to 30% efficiency gains."},
  {"question": "How do you apply for a Pace Port accelerator program?", "answer": "Applications can be submitted via the Pace Port portal, followed by a screening call, technical evaluation, and final pitch to the expert panel."},
  {"question": "What future trends is Pace Port focusing on?", "answer": "Pace Port is exploring quantum computing, extended reality (XR), decentralized finance (DeFi), and sustainable tech innovations for the next wave of digital disruption."},
]

@router.get(
  "/faq",
  response_model=List[InfoItem],
  summary="Fetch the list of innovation FAQ items from TCS Pace Port"
)
async def get_information() -> List[InfoItem]:
  """
  Retrieve the full list of innovation questions and answers.
  """
  return INFORMATION
