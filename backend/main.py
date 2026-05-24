import os
import logging
from typing import List
from fastapi import FastAPI, HTTPException
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
    description=(
        "Decoupled backend microservice powering synthetic customer simulation, "
        "FCA compliance reporting, and media ROI funnel analytics for Tier-1 Retail Banking."
    ),
    version="2.0.0"
)

# Enable Robust CORS Handling
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # Allows all origins for decoupled Vercel/Render hosting
    allow_credentials=True,
    allow_methods=["*"],       # Allows all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],       # Allows all HTTP headers
)

# ---------------------------------------------------------------------------
# Pydantic Schemas — Request & Structured Output Response Models
# ---------------------------------------------------------------------------

class PersonalizeRequest(BaseModel):
    directive: str = Field(
        ...,
        description=(
            "Plain English Credit Card Marketing Directive detailing the strategic "
            "targeting goal (e.g. 'Target high-spend travel customers for our premium "
            "airmiles card with airport VIP lounge benefits.')."
        ),
        examples=[
            "Target high-spend travel segments to cross-sell our premium airmiles card "
            "tier, with priority airport VIP lounge entry and dual flight rewards multiplication."
        ]
    )


# ── Module 1: Synthetic Customer Audience Profiles ──────────────────────────

class CampaignContent(BaseModel):
    email_subject: str = Field(
        ...,
        description=(
            "High-converting, cohort-level email subject line aligned with the directive "
            "segment. Must feel aspirational and premium."
        )
    )
    email_body: str = Field(
        ...,
        description=(
            "Comprehensive, professional, compliance-safe email body tailored to the "
            "target segment. Must look premium with appropriate placeholders like "
            "[Customer Name]. No specific transaction figures or locations in copy."
        )
    )
    push_notification: str = Field(
        ...,
        description=(
            "Unified cohort push notification copy. Must be high-impact and strictly "
            "under 120 characters."
        )
    )
    sms_text: str = Field(
        ...,
        description=(
            "Short, crisp SMS campaign alert with a clear call to action. Must be "
            "strictly under 160 characters."
        )
    )
    creative_asset_token: str = Field(
        ...,
        description=(
            "Unified visual asset token. MUST be exactly one of: 'airplane', "
            "'cashback-wallet', 'luxury-dining', or 'safebox-savings'."
        )
    )


class CustomerProfile(BaseModel):
    customer_id: str = Field(
        ...,
        description="Unique simulated credit customer identifier (format: CUST-XXXX)."
    )
    age: int = Field(
        ...,
        description="Simulated age of the customer (realistic credit profile range: 18–75)."
    )
    location: str = Field(
        ...,
        description=(
            "Simulated geographic location. Major UK cities only "
            "(e.g. London, Manchester, Edinburgh, Bristol, Leeds)."
        )
    )
    segment: str = Field(
        ...,
        description=(
            "Explicit credit card preference segment. MUST be one of: "
            "'High-Flyer Airmiles', 'Cashback Optimizer', "
            "'0% Balance Transfer Switcher', 'Premium Lounge / Dining Seeker', "
            "'Building Credit / Low Revolver'."
        )
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
        description=(
            "Calculated risk score indicating likelihood of switching banks or closing "
            "the card, from 0.0 (no risk) to 100.0 (high risk)."
        )
    )
    # Customer-specific hyper-personalized channel copy
    email_subject: str = Field(
        ...,
        description=(
            "Bespoke hyper-personalized email subject line addressing this customer's "
            "lifestyle signals — no private financial figures."
        )
    )
    email_body: str = Field(
        ...,
        description=(
            "Hyper-personalized email body referencing their lifestyle traits and "
            "segment benefits while remaining fully FCA-compliant. "
            "No specific spend amounts or location tracking in visible copy."
        )
    )
    push_notification: str = Field(
        ...,
        description=(
            "Hyper-personalized push notification tailored to this individual's "
            "behavioral trigger (under 120 characters)."
        )
    )
    sms_text: str = Field(
        ...,
        description=(
            "SMS alert specifically customized for this user. "
            "Under 160 characters with a clear call to action."
        )
    )
    creative_asset_token: str = Field(
        ...,
        description=(
            "Contextual visual asset token for this customer. MUST be exactly one of: "
            "'airplane', 'cashback-wallet', 'luxury-dining', or 'safebox-savings'."
        )
    )


# ── Module 2: FCA Compliance Report ─────────────────────────────────────────

class ComplianceReport(BaseModel):
    status: str = Field(
        ...,
        description=(
            "Overall compliance verdict. MUST be exactly 'APPROVED' if the directive "
            "and all generated copy passes every regulatory check, or 'RISK FLAG' if "
            "any check fails or the directive is potentially high-risk."
        )
    )
    consumer_duty_passed: bool = Field(
        ...,
        description=(
            "True if the campaign copy satisfies the FCA Consumer Duty principle — "
            "ensuring good outcomes for retail customers, clear communications, "
            "and no exploitation of vulnerable groups."
        )
    )
    vulnerable_customer_check: bool = Field(
        ...,
        description=(
            "True if the directive and generated messaging contains appropriate "
            "safeguards for potentially vulnerable customers "
            "(e.g. high debt levels, financial distress signals). "
            "Must be True for directives targeting high-revolver or high-risk segments."
        )
    )
    apr_disclosure_verified: bool = Field(
        ...,
        description=(
            "True if the campaign copy includes or is compatible with mandatory APR "
            "representative rate disclosure per FCA CONC 3 rules on financial promotions."
        )
    )
    executive_summary: str = Field(
        ...,
        description=(
            "A single clear, professional sentence confirming the regulatory status of "
            "this campaign. Written for a non-technical bank executive audience. "
            "Example: 'This campaign complies with all FCA Consumer Duty obligations "
            "and is cleared for immediate live deployment across digital channels.'"
        )
    )


# ── Module 3: Media ROI Funnel Analytics ────────────────────────────────────

class MediaROIFunnel(BaseModel):
    allocated_budget: int = Field(
        ...,
        description=(
            "Total indicative media budget allocated for this campaign in GBP (£). "
            "Generate a realistic figure between £15,000–£75,000 based on directive ambition."
        )
    )
    target_channel: str = Field(
        ...,
        description=(
            "Primary digital media channel recommendation for this directive. "
            "Examples: 'Google Financial Services / Premium Programmatic Networks', "
            "'Meta Audience Network / Lookalike Targeting', "
            "'LinkedIn Sponsored / Wealth Management Tier', "
            "'CRM Email Remarketing / DMP Suppression Layer'."
        )
    )
    impressions: int = Field(
        ...,
        description=(
            "Estimated total campaign impressions. Calculate realistically from the "
            "allocated budget and typical CPM for the target channel "
            "(e.g. premium financial CPM ~£8–£18). "
            "Higher-budget, broad channels drive more impressions."
        )
    )
    ctr_percentage: float = Field(
        ...,
        description=(
            "Estimated click-through rate as a percentage (e.g. 2.45). "
            "Airmiles / premium lifestyle directives typically yield higher CTRs (2.2–3.5%). "
            "Balance-transfer directives yield moderate CTRs (1.5–2.4%) with higher volume."
        )
    )
    completed_signups: int = Field(
        ...,
        description=(
            "Number of completed credit card applications submitted (mid-funnel conversions). "
            "Apply a realistic signup conversion rate of 8–18% of clicks based on directive intent."
        )
    )
    final_approved_accounts: int = Field(
        ...,
        description=(
            "Number of accounts ultimately approved after standard banking credit-risk "
            "underwriting drop-offs. Apply a 35–60% approval rate to completed_signups, "
            "reflecting real-world banking acceptance criteria."
        )
    )
    customer_acquisition_cost: float = Field(
        ...,
        description=(
            "Customer Acquisition Cost in GBP: calculated as allocated_budget / final_approved_accounts. "
            "Round to 2 decimal places."
        )
    )
    projected_net_revenue: int = Field(
        ...,
        description=(
            "Projected net first-year portfolio revenue in GBP from approved accounts. "
            "Use realistic per-account annual revenue assumptions: "
            "Airmiles premium: £320–£420/account, "
            "Balance Transfer: £85–£140/account (tighter margins), "
            "Cashback / Dining: £180–£280/account. "
            "Multiply by final_approved_accounts."
        )
    )


# ── Root Response Model ──────────────────────────────────────────────────────

class PersonalizationResponse(BaseModel):
    campaign_content: CampaignContent = Field(
        ...,
        description=(
            "Global cohort-level campaign content generated for the overall audience "
            "matching the strategic directive."
        )
    )
    customers: List[CustomerProfile] = Field(
        ...,
        description=(
            "List of exactly 5 simulated credit customer profiles tightly matching "
            "the demographic and behavioral traits required by the directive."
        )
    )
    compliance_report: ComplianceReport = Field(
        ...,
        description=(
            "Structured FCA regulatory compliance assessment for this campaign, "
            "covering Consumer Duty, vulnerable customer protections, and APR disclosure."
        )
    )
    media_roi_funnel: MediaROIFunnel = Field(
        ...,
        description=(
            "Full-funnel media ROI projection — from budget allocation through to "
            "approved accounts and net first-year portfolio revenue."
        )
    )


# ---------------------------------------------------------------------------
# API Routes
# ---------------------------------------------------------------------------

@app.get("/")
async def serve_root():
    """
    Root health-check endpoint. Prevents 404s on Render cold-start polling.
    """
    return {
        "status": "online",
        "service": "OmniNexus CDP Personalisation Engine API v2",
        "documentation": "/docs"
    }


@app.get("/api/health")
async def health_check():
    """
    Standard health-check endpoint confirming backend availability
    and GEMINI_API_KEY configuration status.
    """
    api_key_set = bool(os.environ.get("GEMINI_API_KEY"))
    return {
        "status": "healthy",
        "service": "OmniNexus CDP Engine v2",
        "gemini_api_key_configured": api_key_set
    }


@app.post("/api/personalize", response_model=PersonalizationResponse)
async def personalize_cohort(payload: PersonalizeRequest):
    """
    Core MarTech Personalization Endpoint (v2).

    Accepts a plain-English credit card marketing directive, executes a fully-structured
    Gemini 2.5 Flash generation call, and returns:
      - 5 synthetic customer profiles with hyper-personalized omnichannel copy
      - FCA Consumer Duty compliance report
      - Full-funnel media ROI analytics projection
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY is not set in the environment variables.")
        raise HTTPException(
            status_code=500,
            detail=(
                "GEMINI_API_KEY is not configured on this server. "
                "Please add it to your Render environment variables."
            )
        )

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        logger.error("google-genai library is not installed.")
        raise HTTPException(
            status_code=500,
            detail=(
                "The official 'google-genai' library is missing. "
                "Please run: pip install google-genai"
            )
        )

    logger.info(f"Processing v2 personalization request: '{payload.directive}'")

    # ── System Instruction ───────────────────────────────────────────────────
    system_instruction = """
You are a Senior Performance Marketer and Banking Risk Officer at a Tier-1 UK Retail Bank.
You have deep expertise across three disciplines simultaneously:

1. CUSTOMER DATA PLATFORM (CDP) ARCHITECTURE
   - You can synthetically generate highly realistic, demographically coherent credit customer profiles.
   - Profiles must be behaviorally consistent: a high-spend airmiles customer should have low utilisation
     and high avg_spend (£3,000+). A balance-transfer seeker must have high utilisation (65–90%) and elevated churn risk.
   - Each of the 5 profiles must feel like a distinct, real human with a clear story. Vary ages, locations, and behavioral signals.

2. BANK-GRADE COMPLIANCE OFFICER (FCA / UK CONSUMER DUTY)
   - You must evaluate every directive and generated copy against current FCA standards:
     • FCA Consumer Duty (2023): Good outcomes for retail customers, clear and fair communication.
     • CONC 3: Representative APR must be disclosable alongside any financial promotion.
     • Vulnerable Customer Protection: Directives targeting high-revolver or distressed segments
       MUST flag safeguards as active (vulnerable_customer_check = true).
   - Only issue status = "APPROVED" when all three boolean checks pass cleanly.
   - Issue status = "RISK FLAG" if the directive could cause consumer harm or targets an inherently risky segment
     without explicit safeguarding language.
   - The executive_summary must be a single, clear, boardroom-ready sentence.

3. SENIOR PERFORMANCE MEDIA DIRECTOR
   - Allocate a realistic budget between £15,000–£75,000 based on directive ambition and target audience size.
   - Select the most commercially appropriate digital channel for the directive segment.
   - Generate realistic impression volumes using channel-appropriate CPMs:
     • Google Financial Services Premium: CPM ~£12–£18
     • Meta Audience Network / Lookalike: CPM ~£6–£10
     • LinkedIn Sponsored: CPM ~£18–£28 (niche but high-intent)
     • CRM Email Remarketing: CPM equivalent ~£3–£6 (low cost, warm audience)
   - Apply realistic funnel drop-off rates:
     • CTR: Airmiles / Premium Lifestyle = 2.2–3.5% | Balance Transfer = 1.5–2.4% | Dining / Cashback = 1.8–2.8%
     • Signup conversion of clicks: 8–18%
     • Credit approval rate of signups: 35–60%
   - Calculate customer_acquisition_cost = allocated_budget / final_approved_accounts (2 decimal places).
   - Apply realistic per-account annual revenue: Airmiles £320–£420 | Balance Transfer £85–£140 | Dining/Cashback £180–£280.

ABSOLUTE COPY SAFEGUARDS (APPLY TO ALL CUSTOMER-FACING TEXT):
- NEVER mention specific private transaction amounts (e.g. "£4,500 monthly spend").
- NEVER reference specific neighbourhoods or postcodes (e.g. "Mayfair", "SW1").
- NEVER use language that makes a customer feel surveilled or profiled.
- Always use warm, aspirational, lifestyle-driven phrasing.
  ❌ BAD: "Since you spend £4,500 dining in Mayfair..."
  ✅ GOOD: "As someone who values exceptional culinary experiences..."
- Copy must read like it was written by a premium bank's award-winning marketing team.
- Push notifications: strictly under 120 characters. SMS: strictly under 160 characters.
""".strip()

    # ── User Content ─────────────────────────────────────────────────────────
    user_content = (
        f"Please execute the following credit card marketing directive for our board presentation:\n\n"
        f'"{payload.directive}"\n\n'
        f"Generate:\n"
        f"1. Exactly 5 synthetic customer profiles with hyper-personalized omnichannel copy.\n"
        f"2. A unified cohort-level campaign content block.\n"
        f"3. A structured FCA compliance assessment for this campaign.\n"
        f"4. A full-funnel media ROI projection based on the directive's target segment and intent."
    )

    try:
        client = genai.Client(api_key=api_key)

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=user_content,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=PersonalizationResponse,
                system_instruction=system_instruction,
                temperature=0.25,   # Slightly creative but firmly consistent for analytics
            )
        )

        response_text = response.text
        logger.info("Successfully generated structured v2 response from Gemini API.")

        return PersonalizationResponse.model_validate_json(response_text)

    except Exception as e:
        logger.exception("Error communicating with Gemini API or validating structured output.")
        raise HTTPException(
            status_code=502,
            detail=f"Error executing MarTech directive via Gemini API: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
