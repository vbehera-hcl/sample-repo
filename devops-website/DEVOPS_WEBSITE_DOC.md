# DevOps Mastery Program Website - Documentation

## Overview

A modern, responsive website for the DevOps Mastery training program built with HTML, CSS, and JavaScript. Hosted on Firebase with form submissions stored in Firestore and email notifications via EmailJS.

---

## Live Website

**URL**: https://devops-mastery-site-7e429.web.app

**Alternate URL**: https://devops-mastery-site-7e429.firebaseapp.com

---

## Dashboard Links

| Service | URL |
|---------|-----|
| Firebase Console | https://console.firebase.google.com/project/devops-mastery-site-7e429/overview |
| View Enrollments (Firestore) | https://console.firebase.google.com/project/devops-mastery-site-7e429/firestore/data/enrollments |
| EmailJS Dashboard | https://dashboard.emailjs.com |

---

## Project Structure

```
devops-website/
├── index.html          # Main HTML page
├── styles.css          # CSS styling (dark theme, responsive)
├── script.js           # JavaScript (Firebase, EmailJS, animations)
├── firebase.json       # Firebase hosting configuration
├── firestore.rules     # Firestore security rules
├── .firebaserc         # Firebase project configuration
└── DEVOPS_WEBSITE_DOC.md  # This documentation
```

---

## Technology Stack

| Technology | Purpose |
|------------|---------|
| HTML5 | Page structure |
| CSS3 | Styling & animations |
| JavaScript | Interactivity |
| Firebase Hosting | Website hosting (free tier) |
| Firebase Firestore | Database for form submissions |
| EmailJS | Email notifications |
| Font Awesome | Icons |
| Google Fonts (Inter) | Typography |

---

## Features

### Website Sections
- Hero section with animated CI/CD pipeline
- Technologies showcase (Docker, Kubernetes, AWS, Terraform, etc.)
- 7-module curriculum with timeline design
- Features & benefits
- Student testimonials
- 3-tier pricing plans
- Enrollment form
- Footer with navigation

### Form Functionality
- Client-side validation
- Saves to Firebase Firestore
- Sends email notification via EmailJS
- Success/error notifications

---

## Configuration Details

### Firebase Project
- **Project ID**: `devops-mastery-site-7e429`
- **Project Number**: `726356838482`

### EmailJS Configuration
- **Public Key**: `aOpH59p862vi6gbWu`
- **Service ID**: `devops`
- **Template ID**: `devops_mail`

### Firestore Rules
```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /enrollments/{document} {
      allow create: if true;      // Anyone can submit
      allow read, update, delete: if false;  // Admin only via console
    }
  }
}
```

---

## Deployment Commands

### Deploy Full Website
```powershell
cd c:\Users\Viswamohan\Downloads\sample-repo\devops-website
firebase.cmd deploy
```

### Deploy Only Hosting (faster)
```powershell
firebase.cmd deploy --only hosting
```

### Deploy Only Firestore Rules
```powershell
firebase.cmd deploy --only firestore:rules
```

---

## Enrollment Data Structure

Each form submission saves the following data to Firestore:

```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "plan": "pro",
  "timestamp": "2026-01-27T18:00:00Z",
  "source": "https://devops-mastery-site-7e429.web.app"
}
```

---

## Email Notification Template

When someone enrolls, an email is sent with:
- **Subject**: New Enrollment: {name}
- **Body**:
  - Name
  - Email
  - Phone
  - Selected Plan
  - Submission Time

---

## Troubleshooting

### Form Not Submitting
- **Cause**: Browser extensions (ad blockers, password managers)
- **Solution**: Test in Incognito/Private window

### Email Not Sending
- Check EmailJS dashboard for quota (200 free/month)
- Verify Service ID and Template ID are correct

### Website Not Updating After Deploy
- Hard refresh: `Ctrl + Shift + R`
- Clear browser cache

---

## Free Tier Limits

| Service | Free Limit |
|---------|------------|
| Firebase Hosting | 10 GB/month bandwidth |
| Firebase Firestore | 50K reads, 20K writes/day |
| EmailJS | 200 emails/month |

---

## Future Enhancements (Optional)

- [ ] Add Google Analytics
- [ ] Set up custom domain
- [ ] Add payment integration (Stripe)
- [ ] Create admin dashboard
- [ ] Add blog section
- [ ] Implement user authentication

---

## Support

- Firebase Documentation: https://firebase.google.com/docs
- EmailJS Documentation: https://www.emailjs.com/docs/
- Firebase Console: https://console.firebase.google.com

---

**Last Updated**: January 27, 2026
