#!/usr/bin/env node

/**
 * dev.js
 * Sprint Manager CLI - AI-agent based sprint management
 * 
 * This is the refactored entry point that uses the modular architecture.
 * It imports functionality from the modules directory and provides a CLI.
 */

// Add at the very beginning of the file
if (process.env.DEBUG === '1') {
  console.error('DEBUG - dev.js received args:', process.argv.slice(2));
}

import { runCLI } from './modules/commands.js';

// Run the CLI with the process arguments
runCLI(process.argv); 