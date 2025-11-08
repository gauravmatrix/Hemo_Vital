# ============================================================================ #
# COMPLETE AI/ML SERVICES
# ============================================================================ #

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from django.db.models import Count, Sum, Avg, Q
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import joblib
import os
from django.utils import timezone

# Import models
from .models import (
    CustomUser, UserProfile, HospitalProfile, Donation, 
    BloodRequest, BloodStock, AIPredictionLog, DonorAnalytics,
    HospitalAnalytics, GlobalSetting
)

# ============================================================================ #
# 1. BLOOD COMPATIBILITY SERVICE
# ============================================================================ #

def calculate_blood_compatibility_score(donor_blood_group, required_blood_group):
    """
    Calculate blood compatibility score based on medical compatibility rules
    Returns score between 0-30
    """
    compatibility_matrix = {
        'O+': {'O+': 30, 'A+': 25, 'B+': 25, 'AB+': 20, 'O-': 15, 'A-': 10, 'B-': 10, 'AB-': 5},
        'O-': {'O-': 30, 'O+': 25, 'A-': 20, 'B-': 20, 'AB-': 15, 'A+': 10, 'B+': 10, 'AB+': 5},
        'A+': {'A+': 30, 'AB+': 25, 'A-': 20, 'AB-': 15, 'O+': 10, 'O-': 5},
        'A-': {'A-': 30, 'A+': 25, 'AB-': 20, 'AB+': 15, 'O-': 10, 'O+': 5},
        'B+': {'B+': 30, 'AB+': 25, 'B-': 20, 'AB-': 15, 'O+': 10, 'O-': 5},
        'B-': {'B-': 30, 'B+': 25, 'AB-': 20, 'AB+': 15, 'O-': 10, 'O+': 5},
        'AB+': {'AB+': 30, 'AB-': 25, 'A+': 20, 'B+': 20, 'A-': 15, 'B-': 15, 'O+': 10, 'O-': 5},
        'AB-': {'AB-': 30, 'AB+': 25, 'A-': 20, 'B-': 20, 'A+': 15, 'B+': 15, 'O-': 10, 'O+': 5}
    }
    
    if donor_blood_group in compatibility_matrix and required_blood_group in compatibility_matrix[donor_blood_group]:
        return compatibility_matrix[donor_blood_group][required_blood_group]
    return 0

# ============================================================================ #
# 2. INTELLIGENT DONOR MATCHING (ENHANCED)
# ============================================================================ #

def advanced_donor_matching(blood_request, top_n=15):
    """
    Advanced AI-powered donor matching with multiple factors
    """
    hospital = blood_request.hospital
    required_blood = blood_request.blood_group
    urgency = blood_request.urgency
    
    # Get potential donors with same blood group
    potential_donors = CustomUser.objects.filter(
        role=CustomUser.Role.DONOR,
        userprofile__is_available=True,
        userprofile__blood_group__isnull=False
    ).select_related('userprofile')
    
    scored_donors = []
    
    for donor in potential_donors:
        # Calculate comprehensive score
        score = calculate_comprehensive_score(donor, blood_request)
        
        if score >= 40:  # Minimum threshold
            scored_donors.append({
                'donor': donor,
                'score': round(score, 1),
                'match_level': get_match_level(score),
                'reasons': get_match_reasons(donor, blood_request, score),
                'distance': calculate_advanced_location_score(donor.userprofile, hospital.hospitalprofile),
                'last_donation': donor.userprofile.last_donation_date
            })
    
    # Sort by score and return top N
    scored_donors.sort(key=lambda x: x['score'], reverse=True)
    
    # Log AI prediction
    log_ai_prediction(
        prediction_type='DONOR_MATCH',
        user=hospital,
        input_data={
            'blood_request_id': blood_request.id,
            'required_blood': required_blood,
            'urgency': urgency,
            'total_potential_donors': len(potential_donors),
            'qualified_donors': len(scored_donors)
        },
        output_data={
            'top_scores': [d['score'] for d in scored_donors[:5]],
            'average_score': np.mean([d['score'] for d in scored_donors]) if scored_donors else 0
        }
    )
    
    return scored_donors[:top_n]

def calculate_comprehensive_score(donor, blood_request):
    """Calculate comprehensive matching score (0-100)"""
    score_components = {}
    
    # 1. Blood Compatibility (30 points)
    score_components['blood_compatibility'] = calculate_blood_compatibility_score(
        donor.userprofile.blood_group, 
        blood_request.blood_group
    )
    
    # 2. Location Proximity (25 points)
    score_components['location'] = calculate_advanced_location_score(
        donor.userprofile, 
        blood_request.hospital.hospitalprofile
    )
    
    # 3. Donation History & Eligibility (20 points)
    score_components['donation_history'] = calculate_donation_history_score(donor)
    
    # 4. Response Behavior (15 points)
    score_components['response_behavior'] = calculate_response_behavior_score(donor)
    
    # 5. Urgency Multiplier (10 points)
    score_components['urgency'] = calculate_urgency_score(blood_request.urgency)
    
    total_score = sum(score_components.values())
    
    return min(total_score, 100)

def calculate_advanced_location_score(donor_profile, hospital_profile):
    """Advanced location scoring with multiple factors"""
    score = 0
    
    # City match (basic)
    if donor_profile.city and hospital_profile.city:
        if donor_profile.city.lower() == hospital_profile.city.lower():
            score += 15
        elif donor_profile.state and hospital_profile.state:
            if donor_profile.state.lower() == hospital_profile.state.lower():
                score += 10
    
    # Availability radius consideration
    if donor_profile.availability_radius:
        # Simple implementation - could be enhanced with GPS
        score += min(10, donor_profile.availability_radius / 2)
    
    return score

def calculate_donation_history_score(donor):
    """Score based on comprehensive donation history"""
    donations = Donation.objects.filter(donor=donor)
    completed_donations = donations.filter(status=Donation.DonationStatus.COMPLETED)
    
    score = 0
    
    # Number of donations
    donation_count = completed_donations.count()
    if donation_count >= 10:
        score += 10
    elif donation_count >= 5:
        score += 8
    elif donation_count >= 2:
        score += 5
    elif donation_count >= 1:
        score += 3
    
    # Recency of donation
    last_donation = completed_donations.order_by('-donation_date').first()
    if last_donation:
        days_since_last = (timezone.now().date() - last_donation.donation_date).days
        if days_since_last <= 90:
            score += 5  # Recently donated - experienced
        elif days_since_last <= 180:
            score += 3  # Moderately recent
    
    # Consistency (donations per year)
    if donation_count > 0 and last_donation:
        first_donation = completed_donations.order_by('donation_date').first()
        days_active = (last_donation.donation_date - first_donation.donation_date).days
        if days_active > 0:
            donations_per_year = (donation_count / days_active) * 365
            if donations_per_year >= 2:
                score += 5  # Regular donor
    
    return min(score, 20)

def calculate_response_behavior_score(donor):
    """Score based on past response behavior"""
    total_blood_requests = BloodRequest.objects.filter(
        blood_group=donor.userprofile.blood_group,
        created_at__gte=timezone.now() - timedelta(days=180)  # Last 6 months
    ).count()
    
    donor_responses = Donation.objects.filter(
        donor=donor,
        created_at__gte=timezone.now() - timedelta(days=180)
    ).count()
    
    if total_blood_requests > 0:
        response_rate = (donor_responses / total_blood_requests) * 100
        
        if response_rate >= 80:
            return 15
        elif response_rate >= 60:
            return 12
        elif response_rate >= 40:
            return 8
        elif response_rate >= 20:
            return 5
    
    return 3  # Default score for new donors

def calculate_urgency_score(urgency):
    """Score adjustment based on request urgency"""
    urgency_scores = {
        'Critical': 10,
        'Urgent': 7,
        'Normal': 5
    }
    return urgency_scores.get(urgency, 5)

def get_match_level(score):
    """Get human-readable match level"""
    if score >= 80:
        return "Excellent"
    elif score >= 65:
        return "Very Good"
    elif score >= 50:
        return "Good"
    elif score >= 40:
        return "Fair"
    else:
        return "Poor"

def get_match_reasons(donor, blood_request, score):
    """Get reasons for match score"""
    reasons = []
    
    profile = donor.userprofile
    
    # Blood group match
    if calculate_blood_compatibility_score(profile.blood_group, blood_request.blood_group) > 0:
        reasons.append("Blood group compatible")
    
    # Location
    if profile.city and profile.city.lower() == blood_request.hospital.hospitalprofile.city.lower():
        reasons.append("Same city")
    
    # Experience
    donations_count = Donation.objects.filter(donor=donor, status=Donation.DonationStatus.COMPLETED).count()
    if donations_count >= 3:
        reasons.append(f"Experienced donor ({donations_count} donations)")
    
    # Availability
    if profile.is_available:
        reasons.append("Currently available")
    
    return reasons[:3]  # Return top 3 reasons

def find_matching_donors(blood_request):
    """Find matching donors for blood request (legacy compatibility)"""
    matches = advanced_donor_matching(blood_request, top_n=10)
    return [match['donor'] for match in matches]

# ============================================================================ #
# 3. BLOOD DEMAND PREDICTION (ENHANCED)
# ============================================================================ #

def predict_blood_demand_advanced(hospital, days=7):
    """
    Advanced blood demand prediction using multiple factors
    """
    predictions = {}
    
    # Get historical data
    historical_data = get_historical_blood_data(hospital)
    
    for blood_group in UserProfile.BloodGroup.choices:
        blood_data = historical_data.get(blood_group[0], [])
        
        if len(blood_data) >= 7:  # Minimum data points
            # Use multiple prediction methods
            prediction_lr = predict_using_linear_regression(blood_data, days)
            prediction_avg = predict_using_moving_average(blood_data, days)
            prediction_seasonal = predict_using_seasonal_patterns(blood_data, days)
            
            # Combine predictions (weighted average)
            final_prediction = (
                prediction_lr * 0.4 + 
                prediction_avg * 0.3 + 
                prediction_seasonal * 0.3
            )
            
            confidence = calculate_prediction_confidence(blood_data)
            
            predictions[blood_group[0]] = {
                'predicted_demand': max(0, round(final_prediction)),
                'confidence': confidence,
                'confidence_score': confidence['score'],
                'historical_data_points': len(blood_data),
                'trend': get_demand_trend(blood_data),
                'recommendation': generate_stock_recommendation(final_prediction, blood_group[0], hospital)
            }
        else:
            # Fallback to simple prediction
            predictions[blood_group[0]] = predict_blood_demand_simple(hospital, blood_group[0], days)
    
    # Log prediction
    log_ai_prediction(
        prediction_type='DEMAND_PREDICTION',
        user=hospital,
        input_data={
            'hospital_id': hospital.id,
            'prediction_days': days,
            'blood_groups_analyzed': len(predictions)
        },
        output_data={
            'predictions': {bg: data['predicted_demand'] for bg, data in predictions.items()},
            'average_confidence': np.mean([data['confidence_score'] for data in predictions.values()])
        }
    )
    
    return predictions

def predict_blood_demand_simple(hospital, blood_group, days=7):
    """Simple demand prediction fallback"""
    recent_requests = BloodRequest.objects.filter(
        hospital=hospital,
        blood_group=blood_group,
        created_at__gte=timezone.now() - timedelta(days=30)
    )
    
    avg_daily_demand = recent_requests.aggregate(
        avg_demand=Avg('units_required')
    )['avg_demand'] or 1
    
    return {
        'predicted_demand': max(1, round(avg_daily_demand * days)),
        'confidence': {'level': 'Low', 'score': 0.3, 'reason': 'Limited historical data'},
        'confidence_score': 0.3,
        'historical_data_points': recent_requests.count(),
        'trend': 'Stable',
        'recommendation': 'Monitor closely - limited data available'
    }

def get_historical_blood_data(hospital, days=90):
    """Get historical blood request data"""
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=days)
    
    historical_requests = BloodRequest.objects.filter(
        hospital=hospital,
        created_at__date__range=[start_date, end_date]
    )
    
    blood_data = {}
    
    for blood_group in UserProfile.BloodGroup.choices:
        bg_requests = historical_requests.filter(blood_group=blood_group[0])
        
        # Create daily demand data
        daily_demand = []
        current_date = start_date
        
        while current_date <= end_date:
            day_requests = bg_requests.filter(created_at__date=current_date)
            total_units = day_requests.aggregate(total=Sum('units_required'))['total'] or 0
            daily_demand.append(total_units)
            current_date += timedelta(days=1)
        
        blood_data[blood_group[0]] = daily_demand
    
    return blood_data

def predict_using_linear_regression(data, days_to_predict):
    """Predict using linear regression"""
    if len(data) < 2:
        return np.mean(data) if data else 0
    
    X = np.array(range(len(data))).reshape(-1, 1)
    y = np.array(data)
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next days
    future_days = np.array(range(len(data), len(data) + days_to_predict)).reshape(-1, 1)
    predictions = model.predict(future_days)
    
    return max(0, np.mean(predictions))

def predict_using_moving_average(data, days_to_predict, window=7):
    """Predict using moving average"""
    if len(data) < window:
        return np.mean(data) if data else 0
    
    moving_avg = np.convolve(data, np.ones(window)/window, mode='valid')
    return np.mean(moving_avg[-5:]) if len(moving_avg) >= 5 else np.mean(moving_avg)

def predict_using_seasonal_patterns(data, days_to_predict):
    """Predict considering weekly patterns"""
    if len(data) < 14:  # Need at least 2 weeks of data
        return np.mean(data) if data else 0
    
    # Group by day of week
    day_patterns = {}
    for i, value in enumerate(data[-14:]):  # Last 2 weeks
        day_of_week = i % 7
        if day_of_week not in day_patterns:
            day_patterns[day_of_week] = []
        day_patterns[day_of_week].append(value)
    
    # Average by day of week
    day_averages = {day: np.mean(values) for day, values in day_patterns.items()}
    
    # Predict next days based on day patterns
    next_days = [day_averages.get((len(data) + i) % 7, 0) for i in range(days_to_predict)]
    
    return np.mean(next_days)

def calculate_prediction_confidence(data):
    """Calculate confidence score for predictions"""
    if len(data) < 7:
        return {'level': 'Low', 'score': 0.3, 'reason': 'Insufficient historical data'}
    
    # Calculate variance (less variance = more confidence)
    variance = np.var(data)
    if variance == 0:
        confidence_score = 0.9
    else:
        confidence_score = max(0.1, 1 - (variance / (np.mean(data) + 1)))
    
    if confidence_score >= 0.8:
        level = 'High'
    elif confidence_score >= 0.6:
        level = 'Medium'
    else:
        level = 'Low'
    
    return {'level': level, 'score': confidence_score, 'reason': f'Based on {len(data)} data points'}

def get_demand_trend(data):
    """Get demand trend (increasing, decreasing, stable)"""
    if len(data) < 7:
        return 'Insufficient data'
    
    recent_avg = np.mean(data[-7:])
    previous_avg = np.mean(data[-14:-7]) if len(data) >= 14 else np.mean(data[:-7])
    
    if recent_avg > previous_avg * 1.2:
        return 'Increasing'
    elif recent_avg < previous_avg * 0.8:
        return 'Decreasing'
    else:
        return 'Stable'

def generate_stock_recommendation(predicted_demand, blood_group, hospital):
    """Generate stock management recommendations"""
    try:
        current_stock = BloodStock.objects.get(
            hospital=hospital, 
            blood_group=blood_group
        ).units_available
    except BloodStock.DoesNotExist:
        current_stock = 0
    
    stock_ratio = current_stock / (predicted_demand + 1)  # +1 to avoid division by zero
    
    if stock_ratio >= 2.0:
        return "Adequate stock - maintain current levels"
    elif stock_ratio >= 1.0:
        return "Sufficient stock - monitor closely"
    elif stock_ratio >= 0.5:
        return "Low stock - consider replenishment"
    else:
        return "Critical stock - urgent replenishment needed"

# ============================================================================ #
# 4. DONOR ELIGIBILITY & NEXT DONATION PREDICTION
# ============================================================================ #

def predict_next_eligible_date(user):
    """Predict next eligible donation date"""
    if not hasattr(user, 'userprofile'):
        return None
    
    profile = user.userprofile
    
    if not profile.last_donation_date:
        return timezone.now().date()
    
    # Basic eligibility: 90 days gap
    next_date = profile.last_donation_date + timedelta(days=90)
    
    # Adjust based on user health profile
    if profile.weight and profile.weight < 50:
        next_date += timedelta(days=30)  # Additional wait for underweight
    
    return max(next_date, timezone.now().date())

def check_donation_eligibility(user):
    """Check if user is eligible to donate blood"""
    profile = user.userprofile
    
    eligibility = {
        'eligible': True,
        'reasons': [],
        'next_eligible_date': None
    }
    
    # Age check
    if profile.date_of_birth:
        age = (timezone.now().date() - profile.date_of_birth).days // 365
        if age < 18 or age > 65:
            eligibility['eligible'] = False
            eligibility['reasons'].append(f"Age {age} not in 18-65 range")
    
    # Weight check
    if profile.weight and profile.weight < 50:
        eligibility['eligible'] = False
        eligibility['reasons'].append("Weight less than 50kg")
    
    # Donation gap check
    if profile.last_donation_date:
        days_since_last = (timezone.now().date() - profile.last_donation_date).days
        if days_since_last < 90:
            eligibility['eligible'] = False
            eligibility['reasons'].append(f"Last donation was {days_since_last} days ago (90 days required)")
            eligibility['next_eligible_date'] = profile.last_donation_date + timedelta(days=90)
    
    # Availability check
    if not profile.is_available:
        eligibility['eligible'] = False
        eligibility['reasons'].append("Marked as unavailable")
    
    return eligibility

# ============================================================================ #
# 5. DONOR RETENTION & ENGAGEMENT ANALYTICS
# ============================================================================ #

def analyze_donor_retention_risk(hospital=None):
    """
    Comprehensive donor retention risk analysis
    """
    if hospital:
        # Analyze donors for specific hospital
        donors = CustomUser.objects.filter(role=CustomUser.Role.DONOR)
    else:
        # System-wide analysis
        donors = CustomUser.objects.filter(role=CustomUser.Role.DONOR)
    
    retention_analysis = {
        'high_risk': [],
        'medium_risk': [],
        'low_risk': [],
        'summary_stats': {}
    }
    
    for donor in donors:
        risk_analysis = predict_donor_retention_risk(donor)
        
        if risk_analysis['risk_level'] == 'High':
            retention_analysis['high_risk'].append({
                'donor': donor,
                'analysis': risk_analysis
            })
        elif risk_analysis['risk_level'] == 'Medium':
            retention_analysis['medium_risk'].append({
                'donor': donor,
                'analysis': risk_analysis
            })
        else:
            retention_analysis['low_risk'].append({
                'donor': donor,
                'analysis': risk_analysis
            })
    
    # Calculate summary statistics
    total_donors = len(donors)
    retention_analysis['summary_stats'] = {
        'total_donors': total_donors,
        'high_risk_count': len(retention_analysis['high_risk']),
        'medium_risk_count': len(retention_analysis['medium_risk']),
        'low_risk_count': len(retention_analysis['low_risk']),
        'retention_rate': calculate_overall_retention_rate(),
        'avg_engagement_score': calculate_average_engagement_score()
    }
    
    return retention_analysis

def predict_donor_retention_risk(donor):
    """Predict donor retention risk with detailed analysis"""
    risk_factors = []
    risk_score = 0
    
    profile = donor.userprofile
    analytics = getattr(donor, 'analytics', None)
    
    # 1. Donation Activity (35 points max)
    activity_score = analyze_donation_activity(donor)
    risk_score += activity_score['risk_points']
    risk_factors.extend(activity_score['factors'])
    
    # 2. Engagement Metrics (30 points max)
    engagement_score = analyze_engagement_metrics(donor, analytics)
    risk_score += engagement_score['risk_points']
    risk_factors.extend(engagement_score['factors'])
    
    # 3. Profile Completeness (20 points max)
    profile_score = analyze_profile_completeness(profile)
    risk_score += profile_score['risk_points']
    risk_factors.extend(profile_score['factors'])
    
    # 4. Response Behavior (15 points max)
    response_score = analyze_response_behavior(donor)
    risk_score += response_score['risk_points']
    risk_factors.extend(response_score['factors'])
    
    # Determine risk level
    if risk_score >= 60:
        risk_level = "High"
    elif risk_score >= 35:
        risk_level = "Medium" 
    else:
        risk_level = "Low"
    
    # Generate recommendations
    recommendations = generate_retention_recommendations(risk_factors, donor)
    
    analysis = {
        'risk_level': risk_level,
        'risk_score': risk_score,
        'risk_factors': risk_factors[:5],  # Top 5 factors
        'recommendations': recommendations,
        'engagement_score': analytics.engagement_score if analytics else 0,
        'last_activity': analytics.last_activity if analytics else None
    }
    
    return analysis

def analyze_donation_activity(donor):
    """Analyze donation activity patterns"""
    risk_points = 0
    factors = []
    
    donations = Donation.objects.filter(donor=donor)
    completed_donations = donations.filter(status=Donation.DonationStatus.COMPLETED)
    
    # Last donation recency
    last_donation = completed_donations.order_by('-donation_date').first()
    if last_donation:
        days_since_donation = (timezone.now().date() - last_donation.donation_date).days
        
        if days_since_donation > 365:  # 1 year
            risk_points += 25
            factors.append(f"Inactive for {days_since_donation} days")
        elif days_since_donation > 180:  # 6 months
            risk_points += 15
            factors.append(f"No donation in {days_since_donation} days")
    else:
        risk_points += 20
        factors.append("Never donated")
    
    # Donation frequency
    donation_count = completed_donations.count()
    if donation_count == 0:
        risk_points += 10
        factors.append("No donation history")
    
    return {'risk_points': risk_points, 'factors': factors}

def analyze_engagement_metrics(donor, analytics):
    """Analyze engagement metrics"""
    risk_points = 0
    factors = []
    
    if analytics:
        if analytics.engagement_score < 30:
            risk_points += 20
            factors.append(f"Low engagement score ({analytics.engagement_score:.1f})")
        elif analytics.engagement_score < 50:
            risk_points += 10
            factors.append(f"Moderate engagement score ({analytics.engagement_score:.1f})")
        
        # Response rate
        if analytics.response_rate < 0.2:  # 20%
            risk_points += 10
            factors.append(f"Low response rate ({analytics.response_rate:.1%})")
    
    return {'risk_points': risk_points, 'factors': factors}

def analyze_profile_completeness(profile):
    """Analyze profile completeness"""
    risk_points = 0
    factors = []
    
    if profile.profile_completion_score < 70:
        risk_points += 15
        factors.append(f"Incomplete profile ({profile.profile_completion_score}%)")
    
    if not profile.blood_group:
        risk_points += 5
        factors.append("Blood group not specified")
    
    return {'risk_points': risk_points, 'factors': factors}

def analyze_response_behavior(donor):
    """Analyze response behavior to blood requests"""
    risk_points = 0
    factors = []
    
    recent_requests = BloodRequest.objects.filter(
        blood_group=donor.userprofile.blood_group,
        created_at__gte=timezone.now() - timedelta(days=90)
    ).count()
    
    recent_responses = Donation.objects.filter(
        donor=donor,
        created_at__gte=timezone.now() - timedelta(days=90)
    ).count()
    
    if recent_requests > 0:
        response_rate = recent_responses / recent_requests
        if response_rate < 0.1:  # 10%
            risk_points += 10
            factors.append(f"Low recent response rate ({response_rate:.1%})")
    
    return {'risk_points': risk_points, 'factors': factors}

def generate_retention_recommendations(risk_factors, donor):
    """Generate personalized retention recommendations"""
    recommendations = []
    profile = donor.userprofile
    
    # Based on risk factors
    if any("inactive" in factor.lower() or "no donation" in factor.lower() for factor in risk_factors):
        recommendations.append("Send reactivation campaign with impact stories")
    
    if any("engagement" in factor.lower() for factor in risk_factors):
        recommendations.append("Personalized engagement through community events")
    
    if any("profile" in factor.lower() for factor in risk_factors):
        recommendations.append("Profile completion reminder with benefits")
    
    if any("response" in factor.lower() for factor in risk_factors):
        recommendations.append("Priority notifications for matching blood requests")
    
    # General recommendations
    if not recommendations:
        if profile.total_donations == 0:
            recommendations.append("Welcome package and first-time donor guidance")
        elif profile.total_donations < 3:
            recommendations.append("Milestone recognition for next donation")
        else:
            recommendations.append("Loyalty rewards and recognition")
    
    return recommendations[:3]  # Top 3 recommendations

def calculate_overall_retention_rate():
    """Calculate overall donor retention rate"""
    total_donors = CustomUser.objects.filter(role=CustomUser.Role.DONOR).count()
    
    if total_donors == 0:
        return 0
    
    active_donors = CustomUser.objects.filter(
        role=CustomUser.Role.DONOR,
        donations__status=Donation.DonationStatus.COMPLETED,
        donations__donation_date__gte=timezone.now() - timedelta(days=180)
    ).distinct().count()
    
    return (active_donors / total_donors) * 100

def calculate_average_engagement_score():
    """Calculate average engagement score across all donors"""
    donors_with_analytics = CustomUser.objects.filter(
        role=CustomUser.Role.DONOR,
        analytics__isnull=False
    )
    
    if donors_with_analytics.exists():
        avg_score = donors_with_analytics.aggregate(
            avg_score=Avg('analytics__engagement_score')
        )['avg_score'] or 0
        return round(avg_score, 1)
    
    return 0

# ============================================================================ #
# 6. AI PREDICTION LOGGING UTILITY
# ============================================================================ #

def log_ai_prediction(prediction_type, user, input_data, output_data, confidence=0.8):
    """Log AI predictions for monitoring and improvement"""
    AIPredictionLog.objects.create(
        prediction_type=prediction_type,
        target_user=user,
        input_data=input_data,
        output_data=output_data,
        confidence_score=confidence,
        timestamp=timezone.now()
    )

# ============================================================================ #
# 7. ANALYTICS DATA UPDATERS
# ============================================================================ #

def update_donor_analytics(donor):
    """Update analytics for a specific donor"""
    analytics, created = DonorAnalytics.objects.get_or_create(donor=donor)
    
    # Calculate engagement score
    donations_count = donor.donations.filter(status=Donation.DonationStatus.COMPLETED).count()
    profile_completion = donor.userprofile.profile_completion_score
    
    # Simple engagement calculation
    analytics.engagement_score = min(100, (donations_count * 10) + (profile_completion * 0.5))
    analytics.last_activity = timezone.now()
    analytics.save()
    
    return analytics

def update_hospital_analytics(hospital):
    """Update analytics for a specific hospital"""
    analytics, created = HospitalAnalytics.objects.get_or_create(hospital=hospital)
    
    # Calculate fulfillment rate
    total_requests = hospital.blood_requests.count()
    fulfilled_requests = hospital.blood_requests.filter(status='Fulfilled').count()
    
    if total_requests > 0:
        analytics.fulfillment_rate = (fulfilled_requests / total_requests) * 100
    else:
        analytics.fulfillment_rate = 0
    
    analytics.total_requests = total_requests
    analytics.fulfilled_requests = fulfilled_requests
    analytics.last_updated = timezone.now()
    analytics.save()
    
    return analytics