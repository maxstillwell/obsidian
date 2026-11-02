# DocMind Demo Workflow

<!-- founderos-docmind-execution:start -->
## Demo Workflow

### Scenario

A Shopify customer asks: "Where is my order, and can I change my shipping address?"

### Source-grounded answer flow

1. Identify intent: order status plus account/order action.
2. Retrieve approved sources: customer account docs, order status source, merchant policy note.
3. Draft answer with source citations.
4. Check confidence:
   - High: answer directly and cite source.
   - Medium: answer the generic part and ask for needed order/account detail.
   - Low: escalate to human support.
5. Log repeated question and missing source gaps.

### Output Format

- Answer:
- Source used:
- Confidence:
- Escalation needed:
- Follow-up data needed:
- Help center gap:

### Example

Use a source-grounded answer for public/general policy. Do not invent order-specific data unless a private approved integration is available.

### Demo Boundary

This workflow uses public source notes only. Real customer/order data requires a separate approved private-source or API plan.
<!-- founderos-docmind-execution:end -->
