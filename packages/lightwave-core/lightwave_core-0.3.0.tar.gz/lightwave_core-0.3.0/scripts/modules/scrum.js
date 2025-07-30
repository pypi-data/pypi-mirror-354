/**
 * scrum.js
 * Implementation of Lightwave Scrum functionality
 * Provides commands for initializing and managing scrums, sprints, and tasks
 * within the company organizational structure.
 */

import fs from 'fs';
import path from 'path';
import { mkdirSync, writeFileSync, existsSync, readFileSync } from 'fs';
import { format } from 'date-fns';
import { generateTasksFromFile } from './tasks.js';
import { logger } from './logger.js';
import { error, info, success } from './display.js';

/**
 * Initialize a new scrum project with the organizational structure
 * @param {Object} options - Command options
 * @param {string} options.name - Name of the scrum/project
 * @param {string} [options.department="Engineering"] - Department this scrum belongs to
 * @param {string} [options.sprint="sprint-01"] - Initial sprint name
 * @param {string} [options.company="Lightwave"] - Company name
 * @param {string} [options.owners="Joel Schaeffer,Erin Gilchrist"] - Comma-separated list of company owners
 * @param {string} [options.tasksFrom] - Path to initial tasks file to import
 */
export async function initScrum(options) {
  const {
    name,
    department = "Engineering",
    sprint = "sprint-01",
    company = "Lightwave",
    owners = "Joel Schaeffer,Erin Gilchrist",
    tasksFrom
  } = options;

  if (!name) {
    error("Scrum name is required. Use --name=<scrum-name>");
    return;
  }

  info(`Initializing scrum "${name}" in department "${department}"...`);

  // Create directory structure
  const baseDir = process.cwd();
  const companyDir = path.join(baseDir, 'company');
  const departmentDir = path.join(companyDir, 'departments', department);
  const scrumDir = path.join(departmentDir, 'scrums', name);
  const sprintDir = path.join(scrumDir, 'sprints', sprint);
  const tasksDir = path.join(sprintDir, 'tasks');

  // Create directories if they don't exist
  [
    companyDir,
    path.join(companyDir, 'departments'),
    departmentDir,
    path.join(departmentDir, 'scrums'),
    scrumDir,
    path.join(scrumDir, 'sprints'),
    sprintDir,
    tasksDir
  ].forEach(dir => {
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
      logger.debug(`Created directory: ${dir}`);
    }
  });

  // Create configuration files
  const ownersList = owners.split(',').map(owner => owner.trim());
  
  // Company config
  const companyConfig = {
    name: company,
    owners: ownersList,
    administrators: ownersList,
    departments: [department],
    defaultDepartment: department
  };

  // Department config
  const departmentConfig = {
    name: department,
    managers: [ownersList[0]],
    teamMembers: ownersList,
    scrums: [name]
  };

  // Scrum config
  const scrumConfig = {
    name: name,
    department: department,
    scrumMaster: ownersList[0],
    productOwner: ownersList.length > 1 ? ownersList[1] : ownersList[0],
    teamMembers: ownersList,
    activeSprint: sprint,
    sprints: [sprint]
  };

  // Sprint context
  const today = new Date();
  const endDate = new Date(today);
  endDate.setDate(today.getDate() + 14); // 2 weeks sprint
  
  const sprintContext = {
    name: sprint,
    startDate: format(today, 'yyyy-MM-dd'),
    endDate: format(endDate, 'yyyy-MM-dd'),
    goal: `Initial sprint for ${name}`,
    capacity: 40,
    taskLists: ['backlog']
  };

  // Write config files
  writeFileSync(
    path.join(companyDir, 'company-config.json'),
    JSON.stringify(companyConfig, null, 2)
  );

  writeFileSync(
    path.join(departmentDir, 'department-config.json'),
    JSON.stringify(departmentConfig, null, 2)
  );

  writeFileSync(
    path.join(scrumDir, 'scrum-config.json'),
    JSON.stringify(scrumConfig, null, 2)
  );

  writeFileSync(
    path.join(sprintDir, 'sprint-context.json'),
    JSON.stringify(sprintContext, null, 2)
  );

  // Initialize tasks.json
  let tasks = {
    meta: {
      project: name,
      department: department,
      sprint: sprint,
      company: company,
      version: "1.0.0",
      generatedAt: new Date().toISOString()
    },
    tasks: []
  };

  // Import tasks from file if provided
  if (tasksFrom && existsSync(tasksFrom)) {
    try {
      const importedTasks = await generateTasksFromFile(tasksFrom);
      tasks.tasks = importedTasks.tasks || [];
      
      info(`Imported ${tasks.tasks.length} tasks from ${tasksFrom}`);
    } catch (err) {
      error(`Failed to import tasks from ${tasksFrom}: ${err.message}`);
    }
  }

  writeFileSync(
    path.join(tasksDir, 'tasks.json'),
    JSON.stringify(tasks, null, 2)
  );

  // Create global config file to track active scrum/sprint
  const globalConfig = {
    activeCompany: company,
    activeDepartment: department,
    activeScrum: name,
    activeSprint: sprint
  };

  writeFileSync(
    path.join(baseDir, '.lightwave-config.json'),
    JSON.stringify(globalConfig, null, 2)
  );

  success(`Scrum "${name}" initialized successfully!`);
  info(`
  Company: ${company}
  Department: ${department}
  Scrum: ${name}
  Active Sprint: ${sprint}
  
  Directory structure created at:
  ${scrumDir}
  
  To manage tasks in this sprint:
  lightwave sprint use --scrum="${name}" --name="${sprint}"
  lightwave list
  `);
}

/**
 * Create a new sprint within an existing scrum
 * @param {Object} options - Command options
 * @param {string} options.scrum - Scrum this sprint belongs to
 * @param {string} options.name - Name of the sprint
 * @param {string} [options.start] - Sprint start date (YYYY-MM-DD)
 * @param {string} [options.end] - Sprint end date (YYYY-MM-DD)
 * @param {string} [options.goal] - Sprint goal description
 * @param {string} [options.previous] - Previous sprint to copy unfinished tasks from
 * @param {string} [options.department] - Department (defaults to active department)
 */
export async function createSprint(options) {
  const {
    scrum,
    name,
    start,
    end,
    goal,
    previous,
    department
  } = options;

  if (!scrum) {
    error("Scrum name is required. Use --scrum=<scrum-name>");
    return;
  }

  if (!name) {
    error("Sprint name is required. Use --name=<sprint-name>");
    return;
  }

  const baseDir = process.cwd();
  
  // Load global config to get active department if not specified
  let activeDepartment = department;
  if (!activeDepartment) {
    try {
      const globalConfigPath = path.join(baseDir, '.lightwave-config.json');
      if (existsSync(globalConfigPath)) {
        const globalConfig = JSON.parse(readFileSync(globalConfigPath, 'utf8'));
        activeDepartment = globalConfig.activeDepartment;
      }
    } catch (err) {
      logger.error(`Failed to read global config: ${err.message}`);
    }
  }

  if (!activeDepartment) {
    error("Department is required. Use --department=<department>");
    return;
  }

  info(`Creating sprint "${name}" for scrum "${scrum}" in department "${activeDepartment}"...`);

  const companyDir = path.join(baseDir, 'company');
  const departmentDir = path.join(companyDir, 'departments', activeDepartment);
  const scrumDir = path.join(departmentDir, 'scrums', scrum);
  const sprintDir = path.join(scrumDir, 'sprints', name);
  const tasksDir = path.join(sprintDir, 'tasks');

  // Verify scrum exists
  if (!existsSync(scrumDir)) {
    error(`Scrum "${scrum}" not found in department "${activeDepartment}"`);
    return;
  }

  // Create sprint directory
  if (!existsSync(sprintDir)) {
    mkdirSync(sprintDir, { recursive: true });
  }

  // Create tasks directory
  if (!existsSync(tasksDir)) {
    mkdirSync(tasksDir, { recursive: true });
  }

  // Calculate sprint dates
  const today = new Date();
  const startDate = start ? new Date(start) : today;
  
  let endDate;
  if (end) {
    endDate = new Date(end);
  } else {
    endDate = new Date(startDate);
    endDate.setDate(startDate.getDate() + 14); // 2 weeks sprint by default
  }

  // Create sprint context
  const sprintContext = {
    name: name,
    startDate: format(startDate, 'yyyy-MM-dd'),
    endDate: format(endDate, 'yyyy-MM-dd'),
    goal: goal || `Sprint for ${scrum}`,
    capacity: 40,
    taskLists: ['backlog']
  };

  // Write sprint context file
  writeFileSync(
    path.join(sprintDir, 'sprint-context.json'),
    JSON.stringify(sprintContext, null, 2)
  );

  // Update scrum config to include the new sprint
  const scrumConfigPath = path.join(scrumDir, 'scrum-config.json');
  if (existsSync(scrumConfigPath)) {
    try {
      const scrumConfig = JSON.parse(readFileSync(scrumConfigPath, 'utf8'));
      
      if (!scrumConfig.sprints.includes(name)) {
        scrumConfig.sprints.push(name);
      }
      
      // Don't change active sprint automatically
      
      writeFileSync(
        scrumConfigPath,
        JSON.stringify(scrumConfig, null, 2)
      );
    } catch (err) {
      logger.error(`Failed to update scrum config: ${err.message}`);
    }
  }

  // Initialize tasks.json
  let tasks = {
    meta: {
      project: scrum,
      department: activeDepartment,
      sprint: name,
      version: "1.0.0",
      generatedAt: new Date().toISOString()
    },
    tasks: []
  };

  // Copy unfinished tasks from previous sprint if specified
  if (previous) {
    const previousSprintDir = path.join(scrumDir, 'sprints', previous);
    const previousTasksPath = path.join(previousSprintDir, 'tasks', 'tasks.json');
    
    if (existsSync(previousTasksPath)) {
      try {
        const previousTasks = JSON.parse(readFileSync(previousTasksPath, 'utf8'));
        
        // Copy only non-done tasks
        const unfinishedTasks = previousTasks.tasks.filter(task => task.status !== 'done');
        
        if (unfinishedTasks.length > 0) {
          // Append sprint identifier to dependencies that point to the previous sprint
          unfinishedTasks.forEach(task => {
            if (task.dependencies && task.dependencies.length > 0) {
              task.dependencies = task.dependencies.map(depId => {
                // If it doesn't already have a sprint prefix, add the previous sprint prefix
                if (!depId.includes('.') && !isNaN(parseInt(depId))) {
                  return `${previous}.${depId}`;
                }
                return depId;
              });
            }
          });
          
          tasks.tasks = unfinishedTasks;
          info(`Copied ${unfinishedTasks.length} unfinished tasks from sprint "${previous}"`);
        }
      } catch (err) {
        error(`Failed to copy tasks from previous sprint: ${err.message}`);
      }
    } else {
      error(`Previous sprint "${previous}" not found or has no tasks`);
    }
  }

  // Write tasks.json
  writeFileSync(
    path.join(tasksDir, 'tasks.json'),
    JSON.stringify(tasks, null, 2)
  );

  success(`Sprint "${name}" created successfully for scrum "${scrum}"!`);
  info(`
  Department: ${activeDepartment}
  Scrum: ${scrum}
  Sprint: ${name}
  Start Date: ${sprintContext.startDate}
  End Date: ${sprintContext.endDate}
  
  To switch to this sprint:
  lightwave sprint use --scrum="${scrum}" --name="${name}"
  
  To view tasks:
  lightwave list
  `);
}

/**
 * Set the active sprint context for subsequent commands
 * @param {Object} options - Command options
 * @param {string} options.scrum - Scrum name
 * @param {string} options.name - Sprint name
 * @param {string} [options.department] - Department name
 */
export function useSprint(options) {
  const { scrum, name, department } = options;
  
  if (!scrum) {
    error("Scrum name is required. Use --scrum=<scrum-name>");
    return;
  }

  if (!name) {
    error("Sprint name is required. Use --name=<sprint-name>");
    return;
  }

  const baseDir = process.cwd();
  
  // Load global config to get active department if not specified
  let activeDepartment = department;
  let activeCompany = "Lightwave";
  
  try {
    const globalConfigPath = path.join(baseDir, '.lightwave-config.json');
    if (existsSync(globalConfigPath)) {
      const globalConfig = JSON.parse(readFileSync(globalConfigPath, 'utf8'));
      activeDepartment = department || globalConfig.activeDepartment;
      activeCompany = globalConfig.activeCompany;
    }
  } catch (err) {
    logger.error(`Failed to read global config: ${err.message}`);
  }

  if (!activeDepartment) {
    error("Department is required. Use --department=<department>");
    return;
  }

  // Verify sprint exists
  const sprintDir = path.join(
    baseDir, 
    'company', 
    'departments', 
    activeDepartment, 
    'scrums', 
    scrum, 
    'sprints', 
    name
  );

  if (!existsSync(sprintDir)) {
    error(`Sprint "${name}" not found in scrum "${scrum}" in department "${activeDepartment}"`);
    return;
  }

  // Update global config
  const globalConfig = {
    activeCompany,
    activeDepartment,
    activeScrum: scrum,
    activeSprint: name
  };

  writeFileSync(
    path.join(baseDir, '.lightwave-config.json'),
    JSON.stringify(globalConfig, null, 2)
  );

  // Update scrum config to set active sprint
  const scrumConfigPath = path.join(
    baseDir, 
    'company', 
    'departments', 
    activeDepartment, 
    'scrums', 
    scrum, 
    'scrum-config.json'
  );

  if (existsSync(scrumConfigPath)) {
    try {
      const scrumConfig = JSON.parse(readFileSync(scrumConfigPath, 'utf8'));
      scrumConfig.activeSprint = name;
      
      writeFileSync(
        scrumConfigPath,
        JSON.stringify(scrumConfig, null, 2)
      );
    } catch (err) {
      logger.error(`Failed to update scrum config: ${err.message}`);
    }
  }

  success(`Switched to sprint "${name}" in scrum "${scrum}"`);
  info(`
  Active Company: ${activeCompany}
  Active Department: ${activeDepartment}
  Active Scrum: ${scrum}
  Active Sprint: ${name}
  
  All task commands will now operate within this context.
  `);
}

/**
 * Get the active sprint context
 * @returns {Object} The active sprint context or null
 */
export function getActiveSprint() {
  const baseDir = process.cwd();
  const globalConfigPath = path.join(baseDir, '.lightwave-config.json');
  
  if (!existsSync(globalConfigPath)) {
    return null;
  }
  
  try {
    const globalConfig = JSON.parse(readFileSync(globalConfigPath, 'utf8'));
    const { activeCompany, activeDepartment, activeScrum, activeSprint } = globalConfig;
    
    if (!activeCompany || !activeDepartment || !activeScrum || !activeSprint) {
      return null;
    }
    
    return {
      company: activeCompany,
      department: activeDepartment,
      scrum: activeScrum,
      sprint: activeSprint,
      sprintDir: path.join(
        baseDir, 
        'company', 
        'departments', 
        activeDepartment, 
        'scrums', 
        activeScrum, 
        'sprints', 
        activeSprint
      ),
      tasksDir: path.join(
        baseDir, 
        'company', 
        'departments', 
        activeDepartment, 
        'scrums', 
        activeScrum, 
        'sprints', 
        activeSprint,
        'tasks'
      )
    };
  } catch (err) {
    logger.error(`Failed to read global config: ${err.message}`);
    return null;
  }
}

/**
 * Get the tasks path for a specific sprint or the active sprint
 * @param {Object} options - Command options
 * @param {string} [options.scrum] - Scrum name (defaults to active scrum)
 * @param {string} [options.sprint] - Sprint name (defaults to active sprint)
 * @param {string} [options.department] - Department name (defaults to active department)
 * @returns {string|null} The path to the tasks.json file or null
 */
export function getTasksPath(options = {}) {
  const { scrum, sprint, department } = options;
  
  // If no specific sprint is requested, use active sprint
  if (!scrum && !sprint && !department) {
    const activeContext = getActiveSprint();
    
    if (!activeContext) {
      return null;
    }
    
    return path.join(activeContext.tasksDir, 'tasks.json');
  }
  
  // Load global config to fill in missing options
  const baseDir = process.cwd();
  let globalConfig = {};
  
  try {
    const globalConfigPath = path.join(baseDir, '.lightwave-config.json');
    if (existsSync(globalConfigPath)) {
      globalConfig = JSON.parse(readFileSync(globalConfigPath, 'utf8'));
    }
  } catch (err) {
    logger.error(`Failed to read global config: ${err.message}`);
  }
  
  const activeDepartment = department || globalConfig.activeDepartment;
  const activeScrum = scrum || globalConfig.activeScrum;
  const activeSprint = sprint || globalConfig.activeSprint;
  
  if (!activeDepartment || !activeScrum || !activeSprint) {
    return null;
  }
  
  const tasksPath = path.join(
    baseDir, 
    'company', 
    'departments', 
    activeDepartment, 
    'scrums', 
    activeScrum, 
    'sprints', 
    activeSprint,
    'tasks',
    'tasks.json'
  );
  
  return existsSync(tasksPath) ? tasksPath : null;
} 