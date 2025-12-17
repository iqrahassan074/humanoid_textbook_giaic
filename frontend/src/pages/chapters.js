import React from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './chapters.module.css';

function ChapterCard({ title, description, link, number }) {
  return (
    <div className={styles.chapterCard}>
      <div className={styles.chapterHeader}>
        <h3>
          <Link to={link}>
            {number}. {title}
          </Link>
        </h3>
      </div>
      <p className={styles.chapterDescription}>{description}</p>
      <div className={styles.chapterActions}>
        <Link className="button button--primary" to={link}>
          Read Chapter
        </Link>
      </div>
    </div>
  );
}

export default function Chapters() {
  const {siteConfig} = useDocusaurusContext();

  const chapters = [
    {
      number: 1,
      title: "Introduction to Physical AI",
      description: "Explore the fundamental concepts of Physical AI and its historical development.",
      link: "/textbook/introduction-to-physical-ai"
    },
    {
      number: 2,
      title: "Robotics and AI Integration",
      description: "Understand how robotics and artificial intelligence converge to create Physical AI systems.",
      link: "/textbook/robotics-and-ai-integration"
    },
    {
      number: 3,
      title: "Sensorimotor Learning",
      description: "Learn about the sensorimotor loop and how physical systems learn through interaction.",
      link: "/textbook/sensorimotor-learning"
    },
    {
      number: 4,
      title: "Human-Robot Interaction",
      description: "Examine the principles and applications of human-robot interaction in Physical AI.",
      link: "/textbook/human-robot-interaction"
    },
    {
      number: 5,
      title: "Embodied Intelligence",
      description: "Discover how the physical form contributes to intelligent behavior in embodied systems.",
      link: "/textbook/embodied-intelligence"
    },
    {
      number: 6,
      title: "Future of Physical AI",
      description: "Explore the future directions and potential impact of Physical AI technologies.",
      link: "/textbook/future-of-physical-ai"
    }
  ];

  return (
    <Layout
      title={`Textbook Chapters | ${siteConfig.title}`}
      description="Complete Physical AI textbook chapters">
      <main className={styles.main}>
        <div className="container">
          <div className="row">
            <div className="col col--12">
              <header className={styles.header}>
                <h1>Textbook Chapters</h1>
                <p>Browse all chapters of the Physical AI textbook</p>
              </header>
            </div>
          </div>

          <div className="row">
            <div className="col col--12">
              <div className={styles.chaptersGrid}>
                {chapters.map((chapter) => (
                  <ChapterCard
                    key={chapter.number}
                    number={chapter.number}
                    title={chapter.title}
                    description={chapter.description}
                    link={chapter.link}
                  />
                ))}
              </div>
            </div>
          </div>
        </div>
      </main>
    </Layout>
  );
}