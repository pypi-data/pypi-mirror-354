// Import the scrum module functions
import { initScrum, createSprint, useSprint } from './scrum.js';

// Add scrum commands to the commands object
const commands = {
  // ... existing commands ...
  
  // Scrum command - initializes a scrum structure with company organization
  'scrum': {
    description: 'Initialize or manage scrums (projects) in the company structure',
    async action(args) {
      const subcommand = args._[1] || 'help';
      
      switch (subcommand) {
        case 'init':
          return await initScrum({
            name: args.name,
            department: args.department,
            sprint: args.sprint,
            company: args.company,
            owners: args.owners,
            tasksFrom: args.tasksFrom
          });
          
        case 'help':
        default:
          console.log(`
Lightwave Scrum Commands:

  lightwave scrum init --name=<name> [options]    Initialize a new scrum project
    Options:
      --name=<name>              Name of the scrum (required)
      --department=<department>  Department this scrum belongs to (default: "Engineering")
      --sprint=<name>            Initial sprint name (default: "sprint-01")
      --company=<name>           Company name (default: "Lightwave")
      --owners=<list>            Comma-separated owner list (default: "Joel Schaeffer,Erin Gilchrist")
      --tasks-from=<file>        Initial tasks file to import

  lightwave scrum help            Show this help message
          `);
          break;
      }
    }
  },
  
  // Sprint command - manages sprints within scrums
  'sprint': {
    description: 'Create and manage sprints within scrums',
    async action(args) {
      const subcommand = args._[1] || 'help';
      
      switch (subcommand) {
        case 'create':
          return await createSprint({
            scrum: args.scrum,
            name: args.name,
            start: args.start,
            end: args.end,
            goal: args.goal,
            previous: args.previous,
            department: args.department
          });
        
        case 'use':
          return useSprint({
            scrum: args.scrum,
            name: args.name,
            department: args.department
          });
          
        case 'help':
        default:
          console.log(`
Lightwave Sprint Commands:

  lightwave sprint create --scrum=<name> --name=<name> [options]    Create a new sprint
    Options:
      --scrum=<name>             Scrum this sprint belongs to (required)
      --name=<name>              Name of the sprint (required)
      --department=<department>  Department (defaults to active department)
      --start=<date>             Sprint start date (YYYY-MM-DD)
      --end=<date>               Sprint end date (YYYY-MM-DD)
      --goal=<text>              Sprint goal description
      --previous=<name>          Previous sprint to copy unfinished tasks from

  lightwave sprint use --scrum=<name> --name=<name> [options]    Set the active sprint context
    Options:
      --scrum=<name>             Scrum name (required)
      --name=<name>              Sprint name (required)
      --department=<department>  Department name (defaults to active department)

  lightwave sprint help          Show this help message
          `);
          break;
      }
    }
  },
  
  // ... existing commands ...
};

// ... rest of the file ... 