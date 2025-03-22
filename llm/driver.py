from llm import CohereAPI
from dotenv import load_dotenv
import os

load_dotenv()

COHERE_API_KEY = os.environ.get("COHERE_API_KEY")
PINECONE_API_KEY = os.environ.get("PINECONE_API_KEY")

if __name__ == "__main__":
    model = CohereAPI(cohere_api_key=COHERE_API_KEY, pinecone_api_key=PINECONE_API_KEY)

    
    name="Preston High School", 
    data="""Request for Proposal (RFP)
    Preston High School – New Building Construction Project

    Project Overview
    Preston High School is inviting qualified construction firms to submit proposals for the design and construction of a new educational building on the school campus. This new building will support the academic growth and evolving needs of the student body and faculty, fostering a modern, collaborative, and sustainable learning environment.

    The proposed building will include classrooms, specialized labs, meeting areas, administrative offices, and student amenities, designed with the future of education in mind.

    Project Timeline
    RFP Release Date: April 1, 2025

    Mandatory Pre-Proposal Meeting: April 15, 2025 (11:00 AM at Preston High School)

    Deadline for Proposal Submission: May 1, 2025 (5:00 PM)

    Evaluation Period: May 2, 2025 - May 10, 2025

    Contract Award Notification: May 15, 2025

    Construction Start Date: June 1, 2025

    Construction Completion Date: August 1, 2026

    Scope of Work
    Design Phase:

    Collaboration with Preston High School stakeholders to design the building layout and features.

    Conceptual, schematic, and detailed designs to meet the school’s educational requirements and architectural aesthetics.

    Finalization of design with approval from the school board and administration.

    Construction Phase:

    Site preparation, grading, and foundation work.

    Construction of building structure, roofing, interior layout, and exterior features.

    Installation of electrical systems, plumbing, HVAC systems, and fire protection systems.

    Interior finishes, flooring, and furniture installation.

    Landscaping and outdoor amenities.

    Sustainability:

    Integration of sustainable practices, such as energy-efficient systems, low-impact landscaping, and sustainable building materials.

    Compliance with local building codes and LEED (Leadership in Energy and Environmental Design) standards for green buildings.

    Safety and Accessibility:

    Ensure full compliance with local, state, and federal building codes, including ADA (Americans with Disabilities Act) accessibility requirements.

    The building must prioritize student and staff safety, including secure entry points and fire safety systems.

    Proposal Submission Requirements
    All proposals should include the following elements:

    Company Overview:

    Legal name, address, and contact information of the company.

    Overview of the company’s history, expertise, and relevant projects.

    Project Approach:

    Detailed approach to the design and construction of the building.

    Proposed timeline and milestones for the project.

    Sustainability and safety measures to be incorporated into the design and construction process.

    Team Qualifications:

    Resumes and qualifications of key team members (architects, engineers, project managers, etc.).

    Relevant project experience, including at least three similar projects completed in the last five years.

    Cost Proposal:

    Itemized breakdown of the project cost, including design, materials, labor, permits, and any additional fees.

    Payment schedule and terms.

    References:

    Contact information for at least three references from clients for whom the firm has completed similar projects.

    Proposal Evaluation Criteria
    Proposals will be evaluated based on the following criteria:

    Experience and Qualifications: Experience in school building construction and expertise of the proposed project team.

    Project Approach: Quality and feasibility of the design and construction approach, including timeline, sustainability practices, and safety measures.

    Cost: Total project cost, value for money, and alignment with the budget.

    References and Past Performance: Feedback from past clients and demonstrated ability to deliver quality projects on time and within budget.

    Important Information
    Pre-Proposal Meeting:
    All interested parties must attend a mandatory pre-proposal meeting on April 15, 2025 at 11:00 AM at Preston High School. Failure to attend will disqualify the bidder from submitting a proposal.

    Proposal Submission Deadline:
    All proposals must be submitted by May 1, 2025 at 5:00 PM. Late submissions will not be considered.

    Proposal Submission Address:
    Proposals must be submitted in a sealed envelope to:
    Preston High School
    Attn: New Building Construction Proposal
    1234 Preston Ave,
    City, Province, Postal Code

    Questions and Clarifications:
    Any questions regarding the RFP should be directed to the project coordinator, Jane Doe, at (555) 123-4567 or via email at jane.doe@prestonhs.ca. All questions must be submitted no later than April 22, 2025.

    Contract Award and Final Agreement
    The successful bidder will be notified by May 15, 2025. A contract will be signed between Preston High School and the selected contractor, detailing terms and conditions, project milestones, and expectations for both parties.

    Preston High School reserves the right to reject any or all proposals, negotiate with any or all proposers, or waive any irregularities or technicalities in the proposals"""
    model.addDocument(
        name=name,
        data=data
    )
    
    # sys_prompt = """"You are a helpful assistant designed to generate clear, precise, and actionable responses to prompts. Your task is to understand the input and provide relevant, comprehensive answers based on your knowledge and capabilities. When handling tasks like writing documents, proposals, or technical content, ensure that the output is professional, coherent, and well-structured. For all responses, prioritize clarity and accuracy, and maintain a tone appropriate for the context."""
    # sys_prompt = "Return clear metadata"
    human_prompt = """Return the details of proposals related to construction"""

    res = model.retrieveDocuments(
        # context=sys_prompt,
        prompt=human_prompt
    )

    print(res)