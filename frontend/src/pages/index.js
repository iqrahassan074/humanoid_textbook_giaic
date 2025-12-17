import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">{siteConfig.tagline}</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/chapters">
            Read Textbook
          </Link>
          <Link
            className="button button--primary button--lg"
            to="/chatbot"
            style={{ marginLeft: '1rem' }}>
            AI Assistant
          </Link>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Hello from ${siteConfig.title}`}
      description="AI-Powered Physical AI Textbook with Q&A Assistant">
      <HomepageHeader />
      <main>
        <section className={styles.features}>
          <div className="container">
            <div className="row">
              <div className="col col--4">
                <div className="text--center padding-horiz--md">
                  <img src="/img/logo.png" alt="logo"  className={styles.featureImage} />
                  <h3>Comprehensive Content</h3>
                  <p>6 detailed chapters covering all aspects of Physical AI, from fundamentals to future applications.</p>
                </div>
              </div>
              <div className="col col--4">
                <div className="text--center padding-horiz--md">
                  <img src="/img/logo.png" alt="logo"  className={styles.featureImage} />
                  <h3>AI-Powered Assistance</h3>
                  <p>Ask questions about the textbook content and receive answers with proper citations to source material.</p>
                </div>
              </div>
              <div className="col col--4">
                <div className="text--center padding-horiz--md">
                  <img src="/img/logo.png" alt="logo"  className={styles.featureImage} />
                  <h3>Interactive Learning</h3>
                  <p>Engage with the material through our AI assistant, making learning more dynamic and personalized.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className={styles.features} style={{ padding: '2rem 0' }}>
          <div className="container">
            <div className="row">
              <div className="col col--6">
                <h2>What is Physical AI?</h2>
                <p>
                  Physical AI represents the convergence of artificial intelligence and physical systems.
                  It encompasses the development of AI systems that can understand, interact with, and
                  manipulate the physical world. Unlike traditional AI that operates primarily in digital
                  spaces, Physical AI bridges the gap between computational intelligence and tangible reality.
                </p>
                <p>
                  This textbook explores the principles, applications, and future of Physical AI, providing
                  students and researchers with a comprehensive understanding of this emerging field.
                </p>
              </div>
              <div className="col col--6">
                <h2>How It Works</h2>
                <p>
                  Our platform combines a comprehensive textbook with an AI assistant that has been trained
                  specifically on the textbook content. The AI uses a Retrieval-Augmented Generation (RAG)
                  approach to ensure all answers are grounded in the textbook material.
                </p>
                <ul>
                  <li>Zero hallucination - answers only from indexed content</li>
                  <li>Proper citations for all information sources</li>
                  <li>Context-aware responses</li>
                  <li>Confidence scoring for answer reliability</li>
                </ul>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}
