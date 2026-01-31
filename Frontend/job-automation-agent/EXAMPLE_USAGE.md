# JobAgent - Example Usage Guide

Complete walkthroughs showing how to use every feature of JobAgent.

---

## User Journey: First Time Using JobAgent

### Step 1: Landing Page
User visits `https://jobagent.vercel.app/`

**What they see:**
- Animated header with navigation
- Large hero section with gradient text animation
- "Get Started" button
- Features showcase
- Smooth scroll animations

**User action:** Clicks "Get Started" button → Navigates to `/register`

---

### Step 2: Registration

**URL:** `https://jobagent.vercel.app/register`

**Form shown:**
```
Email: user@example.com
Password: ••••••••••
Confirm Password: ••••••••••

--- Job Questionnaire ---
What is your current job title? 
  [Senior Software Engineer]

Years of experience?
  [5 years]

What industries interest you?
  [Tech, Finance, Startup]

Preferred job level?
  [Senior / Lead]

Salary expectation?
  [$150,000 - $200,000]

--- Resume Upload ---
📄 Upload your resume (PDF, DOC, DOCX)
[Choose File] resume-2024.pdf

[Create Account]
```

**User fills in details and uploads resume**

**What happens:**
1. Form validation runs
2. Password is hashed
3. User created in Firebase Auth
4. Resume uploaded to Cloud Storage
5. User profile created in Firestore
6. Redirect to `/dashboard`

---

### Step 3: Dashboard - Main Chat Interface

**URL:** `https://jobagent.vercel.app/dashboard`

**Interface:**
```
┌─────────────────────────────────────┐
│  JobAgent Dashboard                 │
│  [Logo]         [Settings] [Logout] │
├─────────────────────────────────────┤
│                                     │
│  Chat with AI Agent                 │
│                                     │
│  User: Can you fill out this form   │
│        https://forms.google.com/... │
│                                     │
│  🤖 [Thinking animation] ...        │
│                                     │
│  AI: I'll analyze that form now...  │
│       Detected fields:              │
│       - Full Name                   │
│       - Email                       │
│       - Experience (textarea)       │
│       - Company (text)              │
│                                     │
│      Auto-filling with your data... │
│      [Thinking animation continues] │
│                                     │
│  AI: Form filled! Here's what I     │
│      filled in:                     │
│      Name: John Smith               │
│      Email: john@example.com        │
│      Experience: 5 years in...      │
│      Company: Previous Corp         │
│                                     │
│  ┌─────────────────────────────────┐│
│  │ Message input...                ││
│  │ [Attach File]  [Send Button]    ││
│  └─────────────────────────────────┘│
└─────────────────────────────────────┘
```

**Example Conversation 1: Google Form**

```
User: "Here's a Google Form I need to fill: 
https://forms.google.com/d/e/1FAIpQLSd..."

[Thinking animation with bouncing dots appears]

AI: "I've analyzed the form. It has:
- Full Name (required)
- Email (required)  
- Phone (optional)
- Why join this company? (textarea)
- Salary expectation (select)

Let me fill it with your info:
- Name: Using from resume ✓
- Email: Using from profile ✓
- Phone: Using from profile ✓
- Why join: 'I'm interested in...' ✓
- Salary: Using your preference ✓

Ready to submit! Here's the link with 
filled form: [link]"

User: "Great! Submit it"

AI: "Application submitted to the form! 
Check your email for confirmation.
Application saved to your history."
```

**Example Conversation 2: Custom Company Form**

```
User: "Can you help with Acme Corp's 
application? I'll paste the form HTML"

User: [Pastes HTML form]

[Thinking animation]

AI: "Analyzing Acme Corp form...
Found fields:
- Full Name
- LinkedIn Profile
- Cover Letter (textarea)
- Years of Python experience (select)
- Availability (date)

Filling based on your resume and profile...

All filled! Would you like me to:
1. Review the answers before submitting?
2. Submit immediately?
3. Make changes to any field?"

User: "Review first please"

AI: "Here's what I filled:

NAME: John Smith ✓
LINKEDIN: https://linkedin.com/in/john-smith ✓
COVER_LETTER: 'As a senior engineer with 
5+ years experience...' ✓
PYTHON_YEARS: 5+ years ✓
AVAILABILITY: 2024-02-15 ✓

Everything look good?"

User: "Perfect! Submit"

AI: "✓ Application submitted to Acme Corp
Your application has been saved.
Next step: Watch your email for updates"
```

---

### Step 4: Settings Page

**URL:** `https://jobagent.vercel.app/dashboard/settings`

**Interface:**
```
┌─────────────────────────────────────┐
│  Settings                           │
├─────────────────────────────────────┤
│                                     │
│  Profile Information                │
│  ─────────────────────              │
│  Name: [John Smith]                 │
│  Email: john@example.com            │
│  Phone: [+1 (555) 123-4567]        │
│  Location: [San Francisco, CA]      │
│  Bio: [Senior Software Engineer..] │
│                                     │
│  Resume Management                  │
│  ─────────────────────              │
│  Current Resume: resume-2024.pdf    │
│  [Download] [Delete] [Set as Primary]
│                                     │
│  Upload New Resume:                 │
│  [Choose File...] [Upload]          │
│                                     │
│  Job Preferences                    │
│  ─────────────────────              │
│  Title Preference: [Sr. Engineer]   │
│  Industries: [Tech, Finance]        │
│  Salary Range: [$150k - $200k]     │
│  Experience Level: [Senior/Lead]    │
│                                     │
│  [Save Changes] [Logout]            │
│                                     │
└─────────────────────────────────────┘
```

**User actions:**
- Updates phone number
- Uploads new resume version
- Changes salary preference
- Clicks Save

**What happens:**
- Data updated in Firestore
- New resume stored in Cloud Storage
- Preferences saved for AI reference
- Confirmation message shown

---

### Step 5: Applications Page

**URL:** `https://jobagent.vercel.app/dashboard/applications`

**Interface:**
```
┌──────────────────────────────────────────┐
│  My Applications (8 submitted)           │
├──────────────────────────────────────────┤
│                                          │
│  Company    | Position  | Date       | Status
│  ─────────────────────────────────────────
│  Acme Corp  | Sr Eng    | Feb 15     | ✓ Submitted
│  Google     | SWE       | Feb 14     | ✓ Submitted
│  Meta       | Eng Lead  | Feb 13     | ⏳ Pending
│  Amazon     | Principal | Feb 12     | ✓ Submitted
│  OpenAI     | Researcher| Feb 11     | ⏳ Pending
│  Tesla      | Eng Mgr   | Feb 10     | ✓ Submitted
│  Apple      | Sr Eng    | Feb 09     | ⏳ In Review
│  Microsoft  | Manager   | Feb 08     | ✓ Submitted
│                                          │
│  [Filter by Company] [Sort by Date]     │
│                                          │
└──────────────────────────────────────────┘
```

Click on any row to see:
- Application details
- Form URL
- Fields filled
- Date submitted
- Status

---

## AI Agent Examples

### Example 1: LinkedIn-Style Form

```
User: "I found this job on LinkedIn, can you 
help with the application?"

User: [Provides LinkedIn job link]

AI: "Great! I found the job posting for 
Senior Engineer at TechCo. Their application 
form has these fields:

- Full Name
- Email
- Phone
- Work Authorization
- Years of relevant experience
- Why are you interested?
- Upload portfolio/projects
- Preferred start date
- Salary requirements

Filling based on your resume...

[Thinking animation shows]

All fields filled! Your resume shows you have
7 years of Python experience, which matches
perfectly with their requirements.

Ready to submit?"

User: "Yes, submit"

AI: "✓ Application submitted to TechCo
Status: Pending Review
You'll receive updates via email.
Application saved to your history."
```

### Example 2: Custom HTML Form

```
User: "Here's a startup's application form,
can you fill it out?"

User: [Pastes HTML from Greenhouse/Lever]

AI: "Analyzing their form...

Detected company: StartupXYZ
Detected role: Full Stack Engineer

Fields:
- Name
- Email  
- GitHub Profile
- Project experience (3 text fields)
- Cover letter
- Work samples

Filling with your info...

[Thinking animation]

Filled! I used your GitHub profile, 
listed your top 3 projects from your resume,
and generated a tailored cover letter based
on the role description.

Anything you'd like me to adjust?"
```

### Example 3: Multi-Page Application

```
User: "This company has a long application
with 3 pages. Can you handle it?"

AI: "Absolutely! Let me analyze all 3 pages...

[Thinking animation]

Found:
Page 1: Basic Info (5 fields)
Page 2: Experience (textarea + file upload)
Page 3: Additional Questions (6 fields)

I'll fill all pages systematically...

[Thinking animation continues]

All pages filled! Here's summary:

Page 1: Basic info from your profile
Page 2: Experience from resume + portfolio
Page 3: Answers to company-specific questions

Ready?"

User: "Perfect, submit all pages"

AI: "✓ All pages submitted successfully!
Application complete. 
Status saved in your applications list."
```

---

## Error Handling Examples

### Example 1: Form Analysis Fails

```
User: "Can you fill this form?"

User: [Provides URL]

AI: "I had trouble analyzing that form.
It might be behind a login wall or the 
URL is not accessible.

Can you:
1. Paste the form HTML directly?
2. Screenshot the form?
3. Provide another link?"
```

### Example 2: Missing Resume Data

```
User: "Please fill this engineering form"

AI: "I've analyzed the form, but I notice
you haven't provided some information:

- GitHub profile (in settings)
- Portfolio link (in profile)
- Preferred tech stack (in job preferences)

Should I:
1. Fill with default values?
2. Skip these fields?
3. You provide the info now?"
```

### Example 3: Invalid File

```
User: [Tries to upload image as resume]

AI: "I detected that file is an image,
not a document. Supported formats:
- PDF
- DOCX
- DOC

Please upload your resume in one of 
these formats."
```

---

## Advanced Usage

### Batch Applying

```
User: "I want to apply to 10 jobs today.
Can you help with all of them?"

AI: "Absolutely! You can:

1. Send me one job link/form at a time
   and I'll fill each one

2. Provide all 10 links, and I'll:
   - Analyze each form
   - Suggest which ones match your resume
   - Fill them systematically
   - Show you a summary

Which would you prefer?"

User: "Do all 10 at once"

AI: "[Analyzes all 10]

Summary:
✓ 9 forms ready to fill
⚠ 1 form requires specialized info

Starting with top 3 matches:

[Thinking animation - processing form 1]
✓ Form 1 filled (Google - SWE)

[Thinking animation - processing form 2]  
✓ Form 2 filled (Meta - Sr Eng)

[Thinking animation - processing form 3]
✓ Form 3 filled (Amazon - Engineer)

Continue? (3 done, 7 remaining)"

User: "Yes continue"

AI: "[Processes remaining forms]

All 10 applications submitted!

Summary:
- 10 forms filled
- 10 submitted successfully
- 8 matched your profile perfectly
- 2 had minor field mismatches
- Estimated response time: 3-5 days

View all applications in your 
Applications page."
```

### Customizing Answers

```
User: "For the question 'Why are you 
interested in this role?', customize my 
answer to be more specific to their company"

AI: "Sure! What's the company name?"

User: "SpaceX"

AI: "Got it. Here's what I'd suggest:

Current: 'I'm interested in working with 
cutting-edge technology in the aerospace 
industry.'

Improved: 'I'm passionate about SpaceX's 
mission to make life multi-planetary. 
With my 5 years in systems engineering 
and rocket propulsion background, I'm 
excited to contribute to your next 
generation of spacecraft.'"

User: "Perfect, use that"

AI: "✓ Updated and saved!"
```

---

## Performance Tips

**For Users:**
1. Upload resume once - reused for all applications
2. Complete your profile - more accurate form filling
3. Set job preferences - helps AI match better
4. Batch apply - faster than one at a time
5. Review before submitting for important roles

**For Developers:**
1. Cache resume data client-side
2. Batch API requests
3. Show loading states
4. Implement error retry logic
5. Monitor Gemini API quota

---

## Common Questions

**Q: Can it handle LinkedIn applications?**
A: Yes! Just provide the job link and it will analyze and fill LinkedIn's application forms.

**Q: Does it work with Greenhouse/Lever?**
A: Yes! Paste the form HTML and it analyzes all fields automatically.

**Q: Can I apply to multiple jobs at once?**
A: Yes! Provide multiple forms and AI processes them systematically.

**Q: What if a form has custom questions?**
A: AI analyzes each question and provides smart answers based on your resume and profile.

**Q: Is my resume stored safely?**
A: Yes! Stored in Firebase Cloud Storage with security rules restricting access to only your account.

**Q: Can I change responses after submitting?**
A: After submission to external forms, you'd need to contact the company. But you can re-apply with different answers.

---

## Workflow Summary

```
1. Sign Up
   ↓
2. Upload Resume
   ↓
3. Complete Profile
   ↓
4. Go to Dashboard
   ↓
5. Share Job Form/URL with AI
   ↓
6. AI analyzes and auto-fills
   ↓
7. Review filled form
   ↓
8. Submit
   ↓
9. Application saved to history
   ↓
10. Repeat for next job!
```

---

See `/README.md` for more documentation.
