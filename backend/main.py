import os
import logging
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("OmniNexusBackend")

app = FastAPI(
    title="OmniNexus CDP: Autonomous Credit Card Personalisation Engine API",
    description="Decoupled backend service powering synthetic customer simulation and personalized compliance-safe copy generation.",
    version="1.0.0"
)

# Enable Robust CORS Handling
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for decoupled hosting flexibility (Vercel/Render)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allows all HTTP headers
)

# ---------------------------------------------------------------------------
# Pydantic Schemas for API Requests & Structured Output Responses
# ---------------------------------------------------------------------------

class PersonalizeRequest(BaseModel):
    directive: str = Field(
        ..., 
        description="The Plain English Credit Card Directive detailing the strategic marketing goal.",
        examples=["Target high-spend travel segments to cross-sell our premium airmiles card tier, or isolate high-revolver users who need a balance transfer card offer."]
    )

class CampaignContent(BaseModel):
    email_subject: str = Field(
        ..., 
        description="High-converting, cohort-level email subject line aligned with the directive segment."
    )
    email_body: str = Field(
        ..., 
        description="Comprehensive, professional, compliance-safe email body tailored to the target segment. Must look premium and have appropriate placeholding like [Customer Name]."
    )
    push_notification: str = Field(
        ..., 
        description="Unified cohort push notification copy (must be high impact and under 120 characters)."
    )
    sms_text: str = Field(
        ..., 
        description="Short, crisp SMS campaign alert (must be under 160 characters, with call to action)."
    )
    creative_asset_token: str = Field(
        ..., 
        description="Unified visual asset token. MUST be exactly one of: 'airplane', 'cashback-wallet', 'luxury-dining', or 'safebox-savings'."
    )

class CustomerProfile(BaseModel):
    customer_id: str = Field(
        ..., 
        description="Unique simulated credit customer identifier (format: CUST-XXXX)."
    )
    age: int = Field(
        ..., 
        description="Simulated age of the customer (realistic credit profile range: 18-75)."
    )
    location: str = Field(
        ..., 
        description="Simulated geographic location (Major cities in the UK, e.g. London, Manchester, Edinburgh, Bristol)."
    )
    segment: str = Field(
        ..., 
        description="Explicit credit card preference segment. MUST match the context. Examples: 'High-Flyer Airmiles', 'Cashback Optimizer', '0% Balance Transfer Switcher', 'Premium Lounge / Dining Seeker', 'Building Credit / Low Revolver'."
    )
    avg_spend: int = Field(
        ..., 
        description="Simulated average monthly credit card spend in GBP (£)."
    )
    utilisation_rate: float = Field(
        ..., 
        description="Simulated credit utilization rate as a percentage (e.g. 12.5 or 85.0)."
    )
    churn_risk_score: float = Field(
        ..., 
        description="Calculated risk score indicating likelihood of switching banks or closing card, from 0.0 to 100.0."
    )
    # Customer specific hyper-personalization copy
    email_subject: str = Field(
        ..., 
        description="Bespoke hyper-personalized email subject line addressing this customer's behavior or location."
    )
    email_body: str = Field(
        ..., 
        description="Hyper-personalized email body referencing their specific traits (e.g. their spend level, utilization, or location) while remaining compliant."
    )
    push_notification: str = Field(
        ..., 
        description="Hyper-personalized push notification specifically tailored to this individual's behavioral trigger."
    )
    sms_text: str = Field(
        ..., 
        description="SMS alert specifically customized for this user (under 160 characters)."
    )
    creative_asset_token: str = Field(
        ..., 
        description="Contextual visual asset token for this customer. MUST be exactly one of: 'airplane', 'cashback-wallet', 'luxury-dining', or 'safebox-savings'."
    )

class PersonalizationResponse(BaseModel):
    campaign_content: CampaignContent = Field(
        ..., 
        description="Global campaign content generated for the overall cohort matching the directive."
    )
    customers: List[CustomerProfile] = Field(
        ..., 
        description="List of exactly 5 simulated credit customer profiles that tightly fit the customer traits required by the directive."
    )

# ---------------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------------

@app.get("/")
async def serve_root():
    """
    Friendly root endpoint returning online API status. Prevents health check 404s.
    """
    return {
        "status": "online",
        "service": "OmniNexus CDP Personalisation Engine API",
        "documentation": "/docs"
    }

@app.get("/api/health")
async def health_check():
    """
    Standard health check endpoint ensuring backend is running and showing the status of the GEMINI_API_KEY.
    """
    api_key_set = bool(os.environ.get("GEMINI_API_KEY"))
    return {
        "status": "healthy",
        "service": "OmniNexus CDP Engine",
        "gemini_api_key_configured": api_key_set
    }

@app.post("/api/personalize", response_model=PersonalizationResponse)
async def personalize_cohort(payload: PersonalizeRequest):
    """
    Core MarTech Personalization Endpoint.
    Accepts a natural language directive, executes a structured query via Gemini 2.5 Flash,
    and returns 5 synthetic profiles along with personalized multi-channel creative copies.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY is not set in the environment variables.")
        raise HTTPException(
            status_code=500,
            detail="GEMINI_API_KEY is not configured on this server. Please add it to your environment variables."
        )

    try:
        # Import the official modern Google GenAI library
        from google import genai
        from google.genai import types
    except ImportError:
        logger.error("google-genai library is not installed.")
        raise HTTPException(
            status_code=500,
            detail="The official 'google-genai' library is missing from the environment. Please run: pip install google-genai"
        )

    logger.info(f"Processing personalization request for directive: '{payload.directive}'")

    try:
        # Initialize GenAI Client
        client = genai.Client(api_key=api_key)

        # Build highly specific system prompt and user contents
        system_instruction = (
            "You are a Principal Enterprise MarTech Architect and Customer Data Specialist for a Tier-1 Retail Bank. "
            "Your job is to parse a credit card marketing directive, synthetically build exactly 5 highly detailed and realistic "
            "customer profiles matching the demographic traits, and generate hyper-personalized copy for multiple channels.\n\n"
            "CRITICAL DESIGN RULES:\n"
            "1. Segment Variety: The 'segment' field must match one of the standard bank categories: 'High-Flyer Airmiles', "
            "'Cashback Optimizer', '0% Balance Transfer Switcher', 'Premium Lounge / Dining Seeker', 'Building Credit / Low Revolver'.\n"
            "2. Asset Token Validation: The 'creative_asset_token' MUST strictly be one of: 'airplane', 'cashback-wallet', "
            "'luxury-dining', or 'safebox-savings'. Choose the token that represents the target value proposition best (e.g. airmiles -> airplane, "
            "dining -> luxury-dining, shopping/cashback -> cashback-wallet, balance transfers/savings/safety -> safebox-savings).\n"
            "3. Demographic Alignment: Ensure average monthly spend, utilization rates, and churn risk scores are highly correlated and realistic. "
            "For example, a high-revolver seeking balance transfers should have a high utilization rate (e.g., 65-90%) and realistic spend. "
            "An airmiles premium customer should have high spend (e.g. £3000+) and low/medium utilization.\n"
            "4. Multi-Channel Copies: Write high-end, elegant copy that sounds exactly like a premium bank's marketing material. "
            "Ensure that push notifications are under 120 characters and SMS is under 160 characters.\n"
            "5. BANK COMPLIANCE & PRIVACY SAFEGUARDS (CRITICAL RULE): Marketing copy must be professional, warm, aspirational, and value-focused. "
            "To prevent the customer from feeling surveilled or 'spooked', you MUST NEVER explicitly mention exact private transaction figures, "
            "specific monthly spend amounts (e.g. £4,500), exact utilization rates, or specific neighborhood locations (e.g. Mayfair, Soho) in the customer-facing copy. "
            "Instead, use soft, lifestyle-aligned, and benefit-driven phrasing. For example: "
            "Instead of 'Since you spend £4,500 on London dining', write 'As someone who enjoys premium dining and culinary experiences, you can now earn...' "
            "Address them professionally by name (e.g., 'Mr. Davies'), but keep all backend financial tracking details and locations strictly out of the copy. "
            "The tone must be welcoming and premium, never creepy or intrusive."
        )

        user_content = (
            f"Please execute the following credit card marketing directive:\n"
            f"\"{payload.directive}\"\n\n"
            f"Create the 5 synthetic profiles and the unified cohort campaign elements."
        )

        # Call Gemini 2.5 Flash using structured output configuration
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_content,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=PersonalizationResponse,
                system_instruction=system_instruction,
                temperature=0.2  # Slightly lower temperature for consistent behavioral correlation
            )
        )

        # Parse the JSON response text
        # Since response_schema was used, the result is guaranteed to follow the Pydantic schema structure.
        response_text = response.text
        logger.info("Successfully generated structured response from Gemini API.")
        
        # FastAPI will automatically validate and serialize this response to the client using PersonalizationResponse
        return PersonalizationResponse.model_validate_json(response_text)

    except Exception as e:
        logger.exception("Error communicating with Gemini API or validating output.")
        raise HTTPException(
            status_code=502,
            detail=f"Error executing MarTech directive via Gemini API: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    # Default to port 8000 (Render compatibility)
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
