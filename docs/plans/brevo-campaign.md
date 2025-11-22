Here’s a clear, actionable set of requirements to automate daily Brevo email campaigns using content generated in a GitHub Hugo repo:

***

### 1. **Prerequisites**

- **Brevo Account:** Access with API key (v3).
- **GitHub Repo:** Generates daily Markdown post using Hugo.
- **Contact List:** Target list exists in Brevo (store List ID).

***

### 2. **Trigger Flow**

- After Markdown is generated:
    - Extract the post’s title and main content.

***

### 3. **Content Preparation**

- Convert Markdown to HTML (required for Brevo email campaigns).
    - Use an appropriate Markdown-to-HTML converter (Python’s `markdown` module, Node’s `marked`, etc.).
- Optional: Add subject line, preheader, or additional footer HTML.

***

### 4. **API Sequence**

**A. Fetch Brevo List ID**
   - Optionally: Use Brevo API GET `/contacts/lists` to validate or discover recipient list ID.

**B. Create Email Campaign**
   - Endpoint: `POST /v3/emailCampaigns`
     - Fields:
       - `sender` (name/email)
       - `name` (campaign name—e.g., post title + date)
       - `subject` (use post title or custom string)
       - `htmlContent` (converted HTML from Markdown)
       - `recipients` (listIds: [your list ID])
       - Optionally: Plain text content, scheduled sending

**C. Send Campaign**
   - Endpoint: `POST /v3/emailCampaigns/{campaignId}/sendNow`
     - Use campaign ID returned from previous step.

***

### 5. **Error Handling and Logging**

- Log success or failure of each API call.
- Retry on failure for network/API errors.
- Record sent campaign IDs and timestamps.

***

### 6. **Security and Secrets**

- Store Brevo API key securely (environment variables or secrets manager).
- Do not log sensitive info.

***

### 7. **Testing**

- Include logic to send campaign to a test list or test recipient before sending to full list, using `POST /v3/emailCampaigns/{campaignId}/sendTest`.

***

### **Summary of API Endpoints to Use**

- GET `/contacts/lists` (optional discovery)
- POST `/v3/emailCampaigns` (create campaign with generated content)
- POST `/v3/emailCampaigns/{campaignId}/sendNow` (trigger campaign to list)
- POST `/v3/emailCampaigns/{campaignId}/sendTest` (optional pre-send test)

***

### **References**
- Official Brevo developer docs (API v3):[1][2][3][4][5][6]

***

#### **Tip for Implementation**
Pass content as HTML, not Markdown, and parameterize subject/title. Reuse sender and list IDs as needed.

This plan gives an AI coder all the concrete requirements needed to automate daily campaign creation and sending from a Hugo-generated Markdown post!

[1](https://github.com/getbrevo/brevo-php)
[2](https://developers.brevo.com/reference/createemailcampaign-1)
[3](https://developers.brevo.com/reference/getting-started-1)
[4](https://community.brevo.com/t/create-email-campaign-with-template-post-request/2418)
[5](https://developers.brevo.com/reference/sendtestemail-1)
[6](https://www.postman.com/postman/integration-flows/request/tdlak1a/create-an-email-campaign)