import React from 'react'
import { Provider, Heading, Subhead } from 'rebass'
import {
  Hero, CallToAction, ScrollDownIndicator, Section, Checklist
} from 'react-landing-page'
import Field from "./PlayingField_Full-1.png";
import "./landing.css"


const featherCheckmark = <svg
  xmlns="http://www.w3.org/2000/svg"
  width="24" height="24"
  viewBox="0 0 24 24"
  fill="none" stroke="currentColor"
  strokeWidth="2"
  strokeLinecap="round"
  strokeLinejoin="round"
>
  <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
  <polyline points="22 4 12 14.01 9 11.01"/>
</svg>

const Landing = props => (
  <main class="hero-section">
  <section class="container">
    <div class="hero-content">
    
      <div class="hero-text">
        {/* <h2 class="hero-welcome-text">Team</h2> */}
        <h1 class="hero-welcome-text">Pick Path Optimization</h1>
        <br></br>
        <p class="hero-text-description">Presented by - Omni-Channel Warriors</p>
        <a href="/route" class="explore-btn">Explore</a>
      </div>
    </div>
  </section>
</main>
)

export default Landing;
