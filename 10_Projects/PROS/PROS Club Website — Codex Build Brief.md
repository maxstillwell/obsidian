# 

## Project Name

Prime Range Outdoor Society Inc. website rebuild.

Short name: PROS

Current website: `https://pros.org.au/`

## Goal

Build the first working framework for a simple private club website that replaces the current WordPress site.

The current WordPress backend feels too complicated. The new system should be easier to maintain, with a clean public website, membership application flow, simple admin dashboard, Stripe membership payment, member-only news, and email updates.

This is not meant to be a complex SaaS platform. It should be a lightweight club management website.

## Tech Stack

Use:

- Next.js App Router
    
- TypeScript
    
- Tailwind CSS
    
- Supabase Auth
    
- Supabase Postgres
    
- Stripe Checkout
    
- Stripe Webhooks
    
- Resend for email
    
- Vercel deployment
    

Avoid:

- WordPress
    
- WooCommerce
    
- complex ecommerce systems
    
- complex membership plugins
    
- over-engineered role systems
    
- forums or social-network features
    
- unnecessary dependencies
    

## Design Direction

The site should feel:

- clean
    
- outdoors-oriented
    
- premium but simple
    
- easy to read
    
- suitable for a private outdoor club
    
- not too corporate
    
- not too flashy
    

Use a simple layout with:

- top navigation
    
- responsive mobile menu
    
- clean cards
    
- large readable typography
    
- clear calls to action
    
- strong spacing
    
- simple admin dashboard sidebar
    

Initial style can use neutral colours, dark green, earthy tones, and off-white backgrounds.

## Core Public Pages

Create these public pages:

1. `/`
    
    - Home page
        
    - Clear description of the club
        
    - Call to action: Apply for Membership
        
    - Secondary call to action: Read News
        
2. `/about`
    
    - Club overview
        
    - Mission
        
    - Values
        
    - Outdoor community focus
        
3. `/membership`
    
    - Explain membership process
        
    - Step 1: Apply
        
    - Step 2: Committee review
        
    - Step 3: Approved applicant receives payment link
        
    - Step 4: Pay annual membership fee
        
    - Step 5: Membership activated
        
    - Button to `/apply`
        
4. `/apply`
    
    - Membership application form
        
    - Store submissions in Supabase
        
    - Show success message after submit
        
5. `/news`
    
    - Public news listing
        
    - Show published public posts only
        
6. `/news/[slug]`
    
    - Individual news post page
        
    - If post is public, anyone can read
        
    - If post is members-only, require active member login
        
7. `/shop`
    
    - Simple placeholder shop page for now
        
    - Mention club merchandise coming soon
        
    - Include future support for Stripe Checkout product links
        
8. `/contact`
    
    - Contact information
        
    - Basic contact form or mailto link
        
9. `/privacy`
    
    - Placeholder privacy policy page
        
10. `/terms`
    

- Placeholder terms, waiver, and disclaimer page
    

## Membership Application Form

Create a membership application form at `/apply`.

Fields:

- full name
    
- email
    
- phone
    
- date of birth
    
- address
    
- emergency contact name
    
- emergency contact phone
    
- outdoor interests
    
- firearms licence information, optional
    
- referral or how applicant heard about PROS
    
- reason for joining
    
- agreement checkbox
    
- privacy consent checkbox
    
- waiver acknowledgement checkbox
    
- typed signature
    
- submitted at
    

Validation:

- use Zod
    
- required fields should be validated
    
- email should be valid
    
- checkboxes must be accepted before submission
    

On submission:

- insert into `applications` table
    
- status should default to `pending`
    
- show a success page or success card
    
- do not automatically create an active member
    
- do not automatically take payment at application stage
    

## User Roles

Keep roles simple.

Use:

- `admin`
    
- `member`
    

Membership statuses:

- `pending`
    
- `approved`
    
- `active`
    
- `expired`
    
- `cancelled`
    
- `rejected`
    

Rules:

- Admin can access `/admin`
    
- Active members can access `/members`
    
- Approved applicants can pay membership fee
    
- Pending or rejected applicants cannot access member-only content
    
- Only active members can view members-only posts
    

## Authentication

Use Supabase Auth.

Preferred login method:

- email magic link
    

Optional later:

- email/password login
    

Create:

- `/login`
    
- `/logout`
    
- `/members`
    

Use middleware or server-side checks to protect:

- `/admin`
    
- `/members`
    
- members-only posts
    

## Admin Dashboard

Create a simple admin dashboard at `/admin`.

Sidebar sections:

- Dashboard
    
- Applications
    
- Members
    
- Posts
    
- Products
    
- Emails
    
- Settings
    

### `/admin`

Show simple summary cards:

- pending applications count
    
- active members count
    
- published posts count
    
- recent applications
    

### `/admin/applications`

Show applications table.

Columns:

- applicant name
    
- email
    
- phone
    
- status
    
- submitted date
    
- actions
    

Actions:

- view
    
- approve
    
- reject
    

### `/admin/applications/[id]`

Show full application details.

Admin actions:

- approve application
    
- reject application
    
- add internal notes
    

When approved:

- update application status to `approved`
    
- create or update a member/profile record with membership status `approved`
    
- allow membership payment
    

When rejected:

- update application status to `rejected`
    
- do not allow payment
    

### `/admin/members`

Show members table.

Columns:

- name
    
- email
    
- status
    
- membership expiry
    
- Stripe customer ID
    
- actions
    

Actions:

- view member
    
- manually update status
    
- mark expired
    
- add notes
    

### `/admin/posts`

Show post list.

Admin can:

- create post
    
- edit post
    
- publish post
    
- unpublish post
    
- choose visibility: `public` or `members_only`
    

### `/admin/posts/new`

Post fields:

- title
    
- slug
    
- excerpt
    
- body
    
- visibility
    
- status
    
- published at
    

For v1, body can be a textarea with Markdown-style text. Do not add a complex CMS yet.

### `/admin/products`

For v1, create a placeholder product admin.

Fields:

- product name
    
- description
    
- price
    
- Stripe price ID
    
- active
    

Do not build complex stock management.

### `/admin/emails`

For v1, create a simple interface to send update emails.

Options:

- send latest post to active members
    
- send custom subject and message to active members
    

Use Resend.

Log sent emails in `email_logs`.

## Stripe Membership Payment

Use Stripe Checkout.

Create route:

- `POST /api/stripe/create-membership-checkout-session`
    

Rules:

- only approved applicants or approved members can create membership checkout
    
- create Stripe Checkout session for annual membership fee
    
- use Stripe Price ID from environment variable
    
- include metadata:
    
    - application_id
        
    - member_id
        
    - email
        
    - payment_type: `membership`
        

After checkout:

- success URL: `/membership/success`
    
- cancel URL: `/membership/cancelled`
    

Create pages:

- `/membership/success`
    
- `/membership/cancelled`
    

Do not store card details.

## Stripe Webhook

Create route:

- `POST /api/stripe/webhook`
    

Handle events:

- `checkout.session.completed`
    
- `customer.subscription.updated`
    
- `customer.subscription.deleted`
    
- `invoice.payment_succeeded`
    
- `invoice.payment_failed`
    

Webhook behaviour:

- verify Stripe webhook signature
    
- find application/member by metadata or Stripe customer ID
    
- create or update payment record
    
- set member status to `active` after successful membership payment
    
- set membership expiry date where possible
    
- log errors clearly
    

Important:

- webhook should be idempotent
    
- avoid duplicate payment records
    
- do not expose service role key to client
    

## Members Area

Create `/members`.

Only active members can access.

Show:

- welcome message
    
- membership status
    
- membership expiry date
    
- members-only updates
    
- link to public news
    
- placeholder for future member resources
    

If user is logged in but not active:

- show membership status page
    
- explain they need approval/payment before access
    

## News and Member Updates

Posts should support:

- public posts
    
- members-only posts
    

Public posts:

- visible on `/news`
    

Members-only posts:

- visible to active members only
    
- can be linked from `/members`
    

Admin publishing flow:

1. Admin creates post
    
2. Admin selects public or members-only
    
3. Admin publishes
    
4. Admin can click “Send update to active members”
    
5. Resend sends email with title, excerpt, and link
    
6. Save `email_sent_at`
    

Do not automatically send email on every publish unless explicitly clicked by admin.

## Shop

For v1:

- create `/shop`
    
- show “Club merchandise coming soon”
    
- prepare product data structure
    
- do not build a full cart
    

For v2 later:

- product listing
    
- product detail page
    
- Stripe Checkout for one-time payments
    
- order records in Supabase
    

## Database Schema

Create SQL migrations for Supabase.

### `profiles`

Fields:

- `id uuid primary key`
    
- `auth_user_id uuid`
    
- `email text unique`
    
- `full_name text`
    
- `phone text`
    
- `role text default 'member'`
    
- `membership_status text default 'pending'`
    
- `stripe_customer_id text`
    
- `membership_started_at timestamptz`
    
- `membership_expires_at timestamptz`
    
- `notes text`
    
- `created_at timestamptz default now()`
    
- `updated_at timestamptz default now()`
    

### `applications`

Fields:

- `id uuid primary key default gen_random_uuid()`
    
- `full_name text not null`
    
- `email text not null`
    
- `phone text`
    
- `date_of_birth date`
    
- `address text`
    
- `emergency_contact_name text`
    
- `emergency_contact_phone text`
    
- `outdoor_interests text`
    
- `firearms_licence_info text`
    
- `referral text`
    
- `reason_for_joining text`
    
- `agreement_accepted boolean default false`
    
- `privacy_accepted boolean default false`
    
- `waiver_accepted boolean default false`
    
- `typed_signature text`
    
- `status text default 'pending'`
    
- `admin_notes text`
    
- `reviewed_at timestamptz`
    
- `created_at timestamptz default now()`
    
- `updated_at timestamptz default now()`
    

### `payments`

Fields:

- `id uuid primary key default gen_random_uuid()`
    
- `profile_id uuid`
    
- `application_id uuid`
    
- `stripe_customer_id text`
    
- `stripe_checkout_session_id text unique`
    
- `stripe_subscription_id text`
    
- `amount integer`
    
- `currency text default 'aud'`
    
- `payment_type text`
    
- `status text`
    
- `paid_at timestamptz`
    
- `created_at timestamptz default now()`
    

### `posts`

Fields:

- `id uuid primary key default gen_random_uuid()`
    
- `title text not null`
    
- `slug text unique not null`
    
- `excerpt text`
    
- `body text`
    
- `visibility text default 'public'`
    
- `status text default 'draft'`
    
- `published_at timestamptz`
    
- `email_sent_at timestamptz`
    
- `created_at timestamptz default now()`
    
- `updated_at timestamptz default now()`
    

### `products`

Fields:

- `id uuid primary key default gen_random_uuid()`
    
- `name text not null`
    
- `description text`
    
- `price integer`
    
- `currency text default 'aud'`
    
- `stripe_price_id text`
    
- `active boolean default true`
    
- `created_at timestamptz default now()`
    
- `updated_at timestamptz default now()`
    

### `email_logs`

Fields:

- `id uuid primary key default gen_random_uuid()`
    
- `subject text`
    
- `audience text`
    
- `post_id uuid`
    
- `recipient_count integer`
    
- `status text`
    
- `provider_message_id text`
    
- `error_message text`
    
- `sent_at timestamptz default now()`
    

## Row Level Security

Enable RLS where appropriate.

Basic rules:

- public can insert applications
    
- public cannot read all applications
    
- admins can read and update applications
    
- members can read their own profile
    
- admins can read and update profiles
    
- public can read published public posts
    
- active members can read published members-only posts
    
- admins can manage posts
    
- admins can manage products
    
- admins can read email logs
    

If RLS is too much for the first scaffold, create clear TODO comments and keep service-role access only in server routes.

## Environment Variables

Create `.env.example`.

Include:

```env
NEXT_PUBLIC_SITE_URL=
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
STRIPE_MEMBERSHIP_PRICE_ID=

RESEND_API_KEY=
RESEND_FROM_EMAIL=
ADMIN_EMAIL=
```

Rules:

- never expose `SUPABASE_SERVICE_ROLE_KEY` to client components
    
- never expose `STRIPE_SECRET_KEY` to client components
    
- only use server routes/server actions for sensitive operations
    

## Suggested Folder Structure

```txt
app/
  page.tsx
  about/page.tsx
  membership/page.tsx
  apply/page.tsx
  news/page.tsx
  news/[slug]/page.tsx
  shop/page.tsx
  contact/page.tsx
  privacy/page.tsx
  terms/page.tsx
  login/page.tsx
  logout/route.ts
  members/page.tsx
  admin/page.tsx
  admin/applications/page.tsx
  admin/applications/[id]/page.tsx
  admin/members/page.tsx
  admin/posts/page.tsx
  admin/posts/new/page.tsx
  admin/products/page.tsx
  admin/emails/page.tsx
  api/stripe/create-membership-checkout-session/route.ts
  api/stripe/webhook/route.ts
  api/email/send-post-update/route.ts

components/
  layout/
  forms/
  admin/
  ui/

lib/
  supabase/
  stripe/
  email/
  auth/
  validators/

supabase/
  migrations/

types/
```

## First Build Scope

For the first framework, build only:

1. Next.js project setup
    
2. Tailwind layout
    
3. public pages
    
4. application form
    
5. Supabase database migrations
    
6. Supabase client/server helpers
    
7. basic admin dashboard shell
    
8. applications list/detail/admin actions
    
9. placeholder members page
    
10. placeholder posts admin
    
11. `.env.example`
    
12. setup instructions in `README.md`
    

Do not implement every Stripe and Resend feature in the first commit if it makes the first version too large.

Instead, create clean placeholder routes and TODOs for:

- Stripe Checkout
    
- Stripe webhook
    
- Resend email sending
    
- shop checkout
    

## Development Instructions

Work in small commits.

Suggested commit sequence:

1. `chore: initialise Next.js app`
    
2. `feat: add public site layout and pages`
    
3. `feat: add Supabase schema migrations`
    
4. `feat: add membership application form`
    
5. `feat: add admin dashboard shell`
    
6. `feat: add application review flow`
    
7. `feat: add auth and protected routes`
    
8. `feat: add Stripe checkout placeholders`
    
9. `feat: add posts structure`
    
10. `docs: add setup instructions`
    

## Acceptance Criteria for First Framework

The first version is successful when:

- site runs locally with `npm run dev`
    
- public pages are accessible
    
- `/apply` form submits to Supabase
    
- admin dashboard exists
    
- admin can view applications
    
- admin can approve/reject applications
    
- database migrations are included
    
- environment variables are documented
    
- code is simple and readable
    
- no WordPress dependency exists
    
- no complex ecommerce is added
    

## README Requirements

Create a `README.md` with:

- project overview
    
- tech stack
    
- local setup
    
- Supabase setup
    
- environment variables
    
- how to run migrations
    
- how to create the first admin user
    
- Stripe setup notes
    
- Resend setup notes
    
- Vercel deployment notes
    
- known TODOs
    

## Important Product Principles

Keep it simple.

This is a club website, not a software platform.

Prioritise:

- clarity
    
- security
    
- maintainability
    
- simple admin workflows
    
- clean database structure
    
- easy deployment
    

Avoid:

- over-engineering
    
- complex abstractions
    
- premature optimisation
    
- unnecessary UI libraries
    
- large CMS integrations
    
- full ecommerce cart in v1
    

## Initial Homepage Copy Draft

Use this temporary copy. It can be edited later.

Title:

Prime Range Outdoor Society Inc.

Subtitle:

A private outdoor society for members who value responsible recreation, safety, community, and respect for the outdoors.

Primary CTA:

Apply for Membership

Secondary CTA:

Read Club News

Membership section:

Membership is by application and committee review. Approved applicants will receive a secure payment link for the annual membership fee. Payment does not automatically approve membership until the committee review is complete.

## Initial Membership Process Copy

Use this temporary copy.

1. Submit your application.
    
2. The committee reviews your application.
    
3. Approved applicants receive a secure membership fee payment link.
    
4. Once payment is confirmed, your membership is activated.
    
5. Active members receive access to member updates and club communications.
    

## Notes

The current WordPress site already has useful content and a completed membership application page. Use it as a content reference, but do not copy WordPress-specific structure or plugins.

The first goal is to create a clean technical foundation that can later replace WordPress.