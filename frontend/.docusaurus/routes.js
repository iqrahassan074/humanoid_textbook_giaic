import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5ff'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '5ba'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', 'a2b'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'c3c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', '156'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '88c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', '000'),
    exact: true
  },
  {
    path: '/chapters',
    component: ComponentCreator('/chapters', '8c9'),
    exact: true
  },
  {
    path: '/chatbot',
    component: ComponentCreator('/chatbot', '522'),
    exact: true
  },
  {
    path: '/login',
    component: ComponentCreator('/login', 'a8c'),
    exact: true
  },
  {
    path: '/register',
    component: ComponentCreator('/register', 'd3b'),
    exact: true
  },
  {
    path: '/textbook',
    component: ComponentCreator('/textbook', '951'),
    routes: [
      {
        path: '/textbook',
        component: ComponentCreator('/textbook', '842'),
        routes: [
          {
            path: '/textbook',
            component: ComponentCreator('/textbook', '70b'),
            routes: [
              {
                path: '/textbook/',
                component: ComponentCreator('/textbook/', '2f7'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/textbook/embodied-intelligence',
                component: ComponentCreator('/textbook/embodied-intelligence', '508'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/textbook/future-of-physical-ai',
                component: ComponentCreator('/textbook/future-of-physical-ai', '610'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/textbook/human-robot-interaction',
                component: ComponentCreator('/textbook/human-robot-interaction', '1fc'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/textbook/introduction-to-physical-ai',
                component: ComponentCreator('/textbook/introduction-to-physical-ai', '6d5'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/textbook/robotics-and-ai-integration',
                component: ComponentCreator('/textbook/robotics-and-ai-integration', 'c78'),
                exact: true,
                sidebar: "textbookSidebar"
              },
              {
                path: '/textbook/sensorimotor-learning',
                component: ComponentCreator('/textbook/sensorimotor-learning', '545'),
                exact: true,
                sidebar: "textbookSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '2e1'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
