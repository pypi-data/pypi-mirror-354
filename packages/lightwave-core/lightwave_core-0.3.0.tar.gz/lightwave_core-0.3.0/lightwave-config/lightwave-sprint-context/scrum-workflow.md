# Lightwave Scrum Ceremonies & Event Workflow

## Overview

This document describes the Lightwave scrum process workflow, including all ceremonies and the progression of work items through various states.

## Key Ceremonies

### Backlog Grooming & Sprint Planning

- The Scrum Master and Product Owner groom the backlog and perform sprint planning with the Scrum team
- Items are evaluated, prioritized, and selected for upcoming sprint work

### Sprint & Daily Stand-up

- Product backlog items are kept in an organized, prioritized backlog
- Daily updates on progress, blockers, and planning during daily stand-up
- During the sprint, team members work on assigned items

### Sprint Review & Retrospective

- Product features are demoed and included in Release Notes
- After the sprint completes, the Scrum Team holds sprint review and retrospective meetings

## Work Item Workflow

### Product Request Flow

1. **Project Idea** → **Product Request**
   - Requestor submits a detailed feature/enhancement through the established channel
   - Initial evaluation occurs based on business value, technical feasibility, and strategic alignment

### Development Flow

2. **Open** → **Considering** → **Scoping** → **Prioritized** → **Add to Sprint**
   - **Open**: New item requiring initial assessment
   - **Considering**: Under evaluation for feasibility and business value
   - **Scoping**: Requirements and effort being defined
   - **Prioritized**: Ready to be added to a sprint
   - **Add to Sprint**: Scheduled for upcoming sprint work
   Decision diamonds:
   - "Do we want to do?" can route to "Not Doing" if decided against
   - Items may be sent to "Awaiting Prioritization" when ready for scheduling

3. **In Design** → **In Development** → **In Review** → **Ready for Deployment**
   - **In Design**: Technical design and planning
   - **In Development**: Active development work
   - **In Review**: Code review and QA
   - **Ready for Deployment**: Complete and ready to be deployed

4. **Release Notes** → **Closed**
   - **Release Notes**: Documentation of changes in the release
   - **Closed**: Work item complete and delivered

### Bug Submission Flow
1. **Defect Detected** → **Bug Submission** → **Open** → **Triage**
   - Bugs are submitted through the Bug Submission form
   - Triage determines next steps

2. **Need More Info** ← → **Gather Info**
   - Additional information may be requested to properly assess the bug

3. Decision points:
   - "Is this reproducible?" → "Not a Bug" if not reproducible
   - "Is this important?" → "Cannot Reproduce" if not important or can't be verified

4. Bugs flow into **Awaiting Prioritization** and then follow the standard development flow

### Continuous Updates
- Updates on status can be provided throughout the product lifecycle by managing the Release Status column field and Comments.

## Sprint Cadence
- Regular sprints with clear start and end dates
- Consistent sprint lengths (typically 2 weeks)
- Sprint ceremonies scheduled at fixed times

## Conduct Sprint Review and Retrospective
- After the sprint completes, the Scrum Team holds sprint review and retrospective meetings
- Focus on what went well, what didn't, and action items for improvement 