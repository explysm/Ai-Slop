const OWNER = 'explysm';
const REPO = 'Ai-Slop';

const projectsContainer = document.getElementById('projects-container');

async function fetchDir(path) {
    const response = await fetch(`https://api.github.com/repos/${OWNER}/${REPO}/contents/${path}?ref=main`);
    if (!response.ok) {
        throw new Error(`Failed to fetch directory ${path}: ${response.statusText}`);
    }
    return await response.json();
}

async function fetchFile(path) {
    const response = await fetch(`https://api.github.com/repos/${OWNER}/${REPO}/contents/${path}?ref=main`);
    if (!response.ok) {
        throw new Error(`Failed to fetch file ${path}: ${response.statusText}`);
    }
    const data = await response.json();
    return JSON.parse(atob(data.content));
}

async function main() {
    try {
        const categories = await fetchDir('categories');
        for (const category of categories) {
            if (category.type === 'dir') {
                const projects = await fetchDir(category.path);
                for (const project of projects) {
                    if (project.type === 'dir') {
                        try {
                            const info = await fetchFile(`${project.path}/info.json`);
                            const projectCard = document.createElement('article');
                            projectCard.innerHTML = `
                                <h3>${info.name}</h3>
                                <p>${info.description}</p>
                                <a href="${info.url}" target="_blank">View Project</a>
                            `;
                            projectsContainer.appendChild(projectCard);
                        } catch (error) {
                            console.error(`Error fetching info.json for ${project.name}:`, error);
                        }
                    }
                }
            }
        }
    } catch (error) {
        console.error('Error fetching categories:', error);
        projectsContainer.innerHTML = '<p>Error loading projects. See console for details.</p>';
    }
}

main();