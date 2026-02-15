// Test script to validate the generated knowledge base
const fs = require('fs');

// Read the generated file
const jsContent = fs.readFileSync('knowledge-base-content.js', 'utf8');

console.log('✓ File loaded successfully');
console.log(`  Size: ${(jsContent.length / 1024).toFixed(2)} KB`);

// Try to evaluate it
let knowledgeBase;
try {
    knowledgeBase = eval('(' + jsContent.match(/const knowledgeBase = (\[[\s\S]*?\]);/)[1] + ')');
    console.log('✓ JavaScript syntax is valid');
} catch (e) {
    console.error('✗ JavaScript syntax error:', e.message);
    process.exit(1);
}

// Check the knowledgeBase array
if (!knowledgeBase) {
    console.error('✗ knowledgeBase variable not defined');
    process.exit(1);
}

console.log(`✓ knowledgeBase array loaded with ${knowledgeBase.length} entries`);

// Validate structure
let errors = 0;
const requiredFields = ['id', 'title', 'category', 'tags', 'content'];

knowledgeBase.forEach((entry, index) => {
    requiredFields.forEach(field => {
        if (!(field in entry)) {
            console.error(`✗ Entry ${index + 1} missing field: ${field}`);
            errors++;
        }
    });
    
    if (entry.tags && !Array.isArray(entry.tags)) {
        console.error(`✗ Entry ${index + 1}: tags must be an array`);
        errors++;
    }
    
    if (entry.content && typeof entry.content !== 'string') {
        console.error(`✗ Entry ${index + 1}: content must be a string`);
        errors++;
    }
});

if (errors === 0) {
    console.log('✓ All entries have valid structure');
} else {
    console.error(`✗ Found ${errors} structural errors`);
    process.exit(1);
}

// Category distribution
const categories = {};
knowledgeBase.forEach(entry => {
    categories[entry.category] = (categories[entry.category] || 0) + 1;
});

console.log('\nCategory distribution:');
Object.entries(categories).sort().forEach(([cat, count]) => {
    console.log(`  ${cat.padEnd(15)}: ${count} articles`);
});

// Content statistics
const contentLengths = knowledgeBase.map(e => e.content.length);
const avgLength = contentLengths.reduce((a, b) => a + b, 0) / contentLengths.length;
const maxLength = Math.max(...contentLengths);
const minLength = Math.min(...contentLengths);

console.log('\nContent statistics:');
console.log(`  Average length: ${avgLength.toFixed(0)} chars`);
console.log(`  Max length:     ${maxLength} chars`);
console.log(`  Min length:     ${minLength} chars`);

// Largest articles
console.log('\nTop 5 largest articles:');
knowledgeBase
    .map((e, i) => ({ title: e.title, length: e.content.length, index: i + 1 }))
    .sort((a, b) => b.length - a.length)
    .slice(0, 5)
    .forEach((e, i) => {
        const truncated = e.title.length > 45 ? e.title.substring(0, 45) + '...' : e.title;
        console.log(`  ${i + 1}. ${truncated.padEnd(48)} (${e.length} chars)`);
    });

console.log('\n✓ All validation checks passed!');
console.log('✓ The knowledge base is ready to use.');
