// @ts-check
/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  textbookSidebar: [
    {
      type: 'doc',
      id: 'index',
      label: '📘 Physical AI Textbook',
    },
    {
      type: 'category',
      label: '📚 Chapters',
      collapsible: false,
      items: [
        'introduction-to-physical-ai',
        'robotics-and-ai-integration',
        'sensorimotor-learning',
        'human-robot-interaction',
        'embodied-intelligence',
        'future-of-physical-ai',
      ],
    },
  ],
};

export default sidebars;
