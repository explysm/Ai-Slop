const OWNER = 'explysm';
const REPO = 'Ai-Slop';

const categoriesList = document.getElementById('categories-list');
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

function displayProjects(projects) {
    projectsContainer.innerHTML = '';
    for (const project of projects) {
        const projectCard = document.createElement('article');
        projectCard.innerHTML = `
            <h3>${project.name}</h3>
            <p>${project.description}</p>
            <a href="${project.url}" target="_blank">View Project</a>
        `;
        projectsContainer.appendChild(projectCard);
    }
}

async function loadProjectsForCategory(categoryPath) {
    try {
        const projects = await fetchDir(categoryPath);
        const projectInfos = [];
        for (const project of projects) {
            if (project.type === 'dir') {
                try {
                    const info = await fetchFile(`${project.path}/info.json`);
                    projectInfos.push(info);
                } catch (error) {
                    console.error(`Error fetching info.json for ${project.name}:`, error);
                }
            }
        }
        displayProjects(projectInfos);
    } catch (error) {
        console.error(`Error loading projects for category ${categoryPath}:`, error);
        projectsContainer.innerHTML = '<p>Error loading projects. See console for details.</p>';
    }
}

async function main() {
    try {
        const categories = await fetchDir('categories');
        categoriesList.innerHTML = '';
        for (const category of categories) {
            if (category.type === 'dir') {
                const categoryItem = document.createElement('li');
                categoryItem.textContent = category.name;
                categoryItem.dataset.path = category.path;
                categoriesList.appendChild(categoryItem);
            }
        }

        const categoryItems = categoriesList.querySelectorAll('li');
        categoryItems.forEach(item => {
            item.addEventListener('click', () => {
                categoryItems.forEach(i => i.classList.remove('active'));
                item.classList.add('active');
                loadProjectsForCategory(item.dataset.path);
            });
        });

        if (categoryItems.length > 0) {
            categoryItems[0].classList.add('active');
            loadProjectsForCategory(categoryItems[0].dataset.path);
        }

    } catch (error) {
        console.error('Error fetching categories:', error);
        categoriesList.innerHTML = '<p>Error loading categories.</p>';
    }
}

main();
