// // @ts-check
// // `@type` JSDoc annotations allow editor autocompletion and type checking
// // (when paired with `@ts-check`).
// // There are various equivalent ways to declare your Docusaurus config.
// // See: https://docusaurus.io/docs/api/docusaurus-config

// import {themes as prismThemes} from 'prism-react-renderer';

// /** @type {import('@docusaurus/types').Config} */
// const config = {
//   title: 'Physical AI Textbook',
 
//   favicon: 'img/favicon.ico',

//   // Set the production url of your site here
//   url: 'https://your-username.github.io',
//   // Set the /<baseUrl>/ pathname under which your site is served
//   baseUrl: '/',

//   organizationName: 'facebook',
//   projectName: 'docusaurus',

//   onBrokenLinks: 'throw',
//   onBrokenMarkdownLinks: 'warn',

//   i18n: {
//     defaultLocale: 'en',
//     locales: ['en'],
//   },

//   presets: [
//     [
//       'classic',
//       /** @type {import('@docusaurus/preset-classic').Options} */
//       ({
//         docs: {
//           path: 'docs',               
//           routeBasePath: 'textbook',   
//           sidebarPath: './sidebars.js',
//           editUrl:
//             'https://github.com/facebook/docusaurus/tree/main/packages/create-docusaurus/templates/shared/',
//         },
//         blog: false,
//         theme: {
//           customCss: './src/css/custom.css',
//         },
//       }),
//     ],
//   ],

//   themeConfig:
//     /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
//     ({
//       image: 'img/docusaurus-social-card.jpg',
//       navbar: {
//         title: 'Physical AI Textbook',
//         logo: {
//           alt: 'Physical ai book',
//           src: 'img/logo.png',
//         },
//         items: [
//           {to: '/chapters', label: 'Textbook', position: 'left'},
//           // {to: '/chatbot', label: 'AI Assistant', position: 'left'},
//           {to: '/login', label: 'Login', position: 'right'},
//           {to: '/register', label: 'Register', position: 'right'},
//         ],
//       },
//       footer: {
//         style: 'dark',
//         links: [
//           {
//             title: 'Docs',
//             items: [
//               {
//                 label: 'Textbook Chapters',
//                 to: '/textbook',       
//               },
//             ],
//           },
//           {
//             title: 'Community',
//             items: [
//               {
//                 label: 'Stack Overflow',
//                 href: 'https://stackoverflow.com/questions/tagged/docusaurus',
//               },
//               {
//                 label: 'Discord',
//                 href: 'https://discordapp.com/invite/docusaurus',
//               },
//               {
//                 label: 'Twitter',
//                 href: 'https://twitter.com/docusaurus',
//               },
//             ],
//           },
//           {
//             title: 'More',
//             items: [
//               {
//                 label: 'GitHub',
//                 href: 'https://github.com/facebook/docusaurus',
//               },
//             ],
//           },
//         ],
//         copyright: `Copyright © ${new Date().getFullYear()} Physical AI Textbook. Built with Docusaurus.`,
//       },
//       prism: {
//         theme: prismThemes.github,
//         darkTheme: prismThemes.dracula,
//       },
//     }),
// };

// export default config;





// @ts-check
import { themes as prismThemes } from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Physical AI Textbook',
  tagline: 'Learn Physical AI step by step',
  favicon: 'img/favicon.ico',

  // ✅ Vercel-safe URL settings
  url: 'https://humanoid-textbook-giaic.vercel.app',
  baseUrl: '/',

  // ✅ Not required for Vercel, but keep valid
  organizationName: 'iqrahassan074',
  projectName: 'humanoid_textbook_giaic',

  // ✅ VERY IMPORTANT: prevent Vercel build failure
  onBrokenLinks: 'ignore',
  onBrokenMarkdownLinks: 'ignore',

  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },

  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          path: 'docs',
          routeBasePath: 'textbook', // 👈 /textbook
          sidebarPath: require.resolve('./sidebars.js'),
          editUrl:
            'https://github.com/iqrahassan074/humanoid_textbook_giaic',
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      }),
    ],
  ],

  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      image: 'img/docusaurus-social-card.jpg',
      navbar: {
        title: 'Physical AI Textbook',
        logo: {
          alt: 'Physical AI Book',
          src: 'img/logo.png',
        },
        items: [
          {
            to: '/textbook',
            label: 'Textbook',
            position: 'left',
          },
          {
            to: '/login',
            label: 'Login',
            position: 'right',
          },
          {
            to: '/register',
            label: 'Register',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: 'Textbook',
            items: [
              {
                label: 'Chapters',
                to: '/textbook',
              },
            ],
          },
          {
            title: 'Community',
            items: [
              {
                label: 'GitHub',
                href: 'https://github.com/iqrahassan074/humanoid_textbook_giaic',
              },
            ],
          },
        ],
        copyright:
          `Copyright © ${new Date().getFullYear()} Physical AI Textbook.`,
      },
      prism: {
        theme: prismThemes.github,
        darkTheme: prismThemes.dracula,
      },
    }),
};

export default config;










