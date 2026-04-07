import React from "react";
import Carousel from './Carousel.js'
import Card from './card-ui'
import Services from './Services.js'
import { Container, Row, Col, Button } from "reactstrap";
import "./App.css";

const TourRecommendationSection = () => (
  <div className="tour-recommendation-section" style={{
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    padding: '80px 0',
    textAlign: 'center',
    margin: '50px 0'
  }}>
    <Container>
      <Row>
        <Col lg="12">
          <h2 className="display-4 mb-4">
            🌟 Discover Your Perfect Indian Adventure
          </h2>
          <p className="lead mb-4">
            Let our AI-powered recommendation system suggest the best destinations for you based on your preferences.
            Explore 100+ incredible places across India!
          </p>
          <div className="recommendation-features mb-4">
            <Row>
              <Col md="4">
                <div className="feature-item mb-3">
                  <div style={{ fontSize: '2em', marginBottom: '10px' }}>🏛️</div>
                  <h5>Historical Monuments</h5>
                  <p>UNESCO World Heritage Sites & Ancient Wonders</p>
                </div>
              </Col>
              <Col md="4">
                <div className="feature-item mb-3">
                  <div style={{ fontSize: '2em', marginBottom: '10px' }}>🏔️</div>
                  <h5>Natural Beauty</h5>
                  <p>Hill Stations, Beaches & Wildlife Sanctuaries</p>
                </div>
              </Col>
              <Col md="4">
                <div className="feature-item mb-3">
                  <div style={{ fontSize: '2em', marginBottom: '10px' }}>🕉️</div>
                  <h5>Spiritual Journey</h5>
                  <p>Sacred Temples & Pilgrimage Sites</p>
                </div>
              </Col>
            </Row>
          </div>
          <div className="recommendation-buttons">
            <a href="/tour-recommendation/" 
               className="btn btn-light btn-lg mr-3" 
               style={{
                 padding: '15px 30px',
                 borderRadius: '25px',
                 fontWeight: 'bold',
                 textDecoration: 'none',
                 color: '#667eea',
                 border: 'none',
                 boxShadow: '0 4px 15px rgba(0,0,0,0.2)'
               }}>
              ✨ Get My Recommendation
            </a>
            <a href="/all-destinations/" 
               className="btn btn-outline-light btn-lg"
               style={{
                 padding: '15px 30px',
                 borderRadius: '25px',
                 fontWeight: 'bold',
                 textDecoration: 'none',
                 border: '2px solid white'
               }}>
              🗺️ Browse All Destinations
            </a>
          </div>
        </Col>
      </Row>
    </Container>
  </div>
);

const Home = () => (
  <div>
      <Carousel/>
      <Card/>
      <TourRecommendationSection/>
      <Services/>
  </div>
);

export default Home;