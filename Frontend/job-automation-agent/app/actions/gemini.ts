'use server';

// Secure server-side Gemini API handler
// API key is never exposed to the client

interface GeminiMessage {
  role: 'user' | 'model';
  parts: Array<{
    text: string;
  }>;
}

interface FormAnalysis {
  fields: Array<{
    name: string;
    type: string;
    required: boolean;
    placeholder?: string;
    value?: string;
  }>;
  companyName?: string;
  jobTitle?: string;
  suggestedAnswers: Record<string, string>;
}

const GEMINI_API_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent';

function getApiKey(): string {
  const key = process.env.GEMINI_API_KEY;
  if (!key) {
    throw new Error('GEMINI_API_KEY environment variable is not set');
  }
  return key;
}

export async function sendGeminiMessage(userMessage: string): Promise<string> {
  try {
    const apiKey = getApiKey();
    
    const systemPrompt = `You are JobAgent, an expert job application assistant. Your role is to:
1. Help users understand job application requirements
2. Analyze job application forms
3. Provide intelligent suggestions for filling out forms based on user's resume
4. Extract information from job postings
5. Generate compelling answers for application questions

When users provide job form URLs or form HTML:
- Analyze the form structure and required fields
- Ask for their resume if not provided
- Suggest how to fill each field
- Help match their experience to job requirements

Be professional, helpful, and thorough. Ask clarifying questions when needed.`;

    const response = await fetch(`${GEMINI_API_URL}?key=${apiKey}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        contents: [
          {
            role: 'user',
            parts: [
              {
                text: userMessage,
              },
            ],
          },
        ],
        systemInstruction: {
          parts: [
            {
              text: systemPrompt,
            },
          ],
        },
        generationConfig: {
          temperature: 0.7,
          maxOutputTokens: 2048,
          topP: 0.95,
        },
      }),
    });

    if (!response.ok) {
      const error = await response.json();
      console.error('[JobAgent] Gemini API error:', error);
      throw new Error(`Gemini API error: ${response.statusText}`);
    }

    const data = await response.json();
    
    if (data.candidates && data.candidates[0]?.content?.parts?.[0]?.text) {
      return data.candidates[0].content.parts[0].text;
    }

    throw new Error('Unexpected Gemini API response format');
  } catch (error) {
    console.error('[JobAgent] Error calling Gemini API:', error);
    throw error;
  }
}

export async function analyzeJobForm(
  formHtml: string,
  resumeText: string
): Promise<FormAnalysis> {
  try {
    const apiKey = getApiKey();
    
    const prompt = `
You are a job application form analyzer. Analyze the following job application form HTML and extract:
1. All form fields with their names and types
2. The company name if visible
3. The job title if visible
4. Suggested answers based on the resume provided

Form HTML:
${formHtml}

Resume:
${resumeText}

Return a JSON object with the following structure:
{
  "fields": [
    {"name": "field_name", "type": "text|email|textarea|select|radio|checkbox", "required": true/false, "placeholder": "..."}
  ],
  "companyName": "...",
  "jobTitle": "...",
  "suggestedAnswers": {
    "field_name": "suggested_value"
  }
}

IMPORTANT: Return ONLY valid JSON, no additional text.`;

    const response = await fetch(`${GEMINI_API_URL}?key=${apiKey}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        contents: [
          {
            role: 'user',
            parts: [
              {
                text: prompt,
              },
            ],
          },
        ],
        generationConfig: {
          temperature: 0.3,
          maxOutputTokens: 2048,
        },
      }),
    });

    if (!response.ok) {
      throw new Error(`Gemini API error: ${response.statusText}`);
    }

    const data = await response.json();
    const responseText = data.candidates?.[0]?.content?.parts?.[0]?.text;

    if (!responseText) {
      throw new Error('No response from Gemini API');
    }

    // Extract JSON from response
    const jsonMatch = responseText.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('Could not parse JSON from Gemini response');
    }

    return JSON.parse(jsonMatch[0]) as FormAnalysis;
  } catch (error) {
    console.error('[JobAgent] Error analyzing form:', error);
    throw error;
  }
}

export async function fillFormWithData(
  formStructure: FormAnalysis,
  userData: Record<string, string>
): Promise<FormAnalysis> {
  try {
    const apiKey = getApiKey();
    
    const prompt = `
You are a job application form filler. Fill out the following form fields with the provided user data.

Form structure:
${JSON.stringify(formStructure, null, 2)}

User data:
${JSON.stringify(userData, null, 2)}

Fill each field intelligently with appropriate data from the user's information.

Return a JSON object with the filled form data:
{
  "fields": [...updated fields with values...],
  "companyName": "...",
  "jobTitle": "...",
  "suggestedAnswers": {
    "field_name": "filled_value"
  }
}

IMPORTANT: Return ONLY valid JSON, no additional text.`;

    const response = await fetch(`${GEMINI_API_URL}?key=${apiKey}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        contents: [
          {
            role: 'user',
            parts: [
              {
                text: prompt,
              },
            ],
          },
        ],
        generationConfig: {
          temperature: 0.2,
          maxOutputTokens: 2048,
        },
      }),
    });

    if (!response.ok) {
      throw new Error(`Gemini API error: ${response.statusText}`);
    }

    const data = await response.json();
    const responseText = data.candidates?.[0]?.content?.parts?.[0]?.text;

    if (!responseText) {
      throw new Error('No response from Gemini API');
    }

    const jsonMatch = responseText.match(/\{[\s\S]*\}/);
    if (!jsonMatch) {
      throw new Error('Could not parse JSON from Gemini response');
    }

    return JSON.parse(jsonMatch[0]) as FormAnalysis;
  } catch (error) {
    console.error('[JobAgent] Error filling form:', error);
    throw error;
  }
}
