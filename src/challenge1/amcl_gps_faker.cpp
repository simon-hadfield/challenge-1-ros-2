/*
 * amcl_gps_faker.cpp
 *
 * Uses the functions from navsat_conversions.h provided by ROS robot_localization package.
 * http://docs.ros.org/hydro/api/robot_localization/html/navsat__conversions_8h_source.html
 *
 * Note: This is a dodgy hack. The scale is completely wrong and was guessed by eye on a small sequence.
 * The correct way to do this conversion is to use something like https://geographiclib.sourceforge.io/html/classGeographicLib_1_1Geocentric.html
 * an example doing this is here https://github.com/mavlink/mavros/blob/master/mavros_extras/src/plugins/fake_gps.cpp
 *
 *  Created on: Jan 28, 2020
 *      Author: Simon Hadfield
 */

#include <iostream>
#include <ros/ros.h>
#include <robot_localization/navsat_conversions.h>
#include <geometry_msgs/PoseWithCovarianceStamped.h>
#include <sensor_msgs/NavSatFix.h>

using namespace std;

bool g_rand_seeded = false;

//uniformly creates a random number from 0 to 1 non-inclusive, srand should be called previously
inline double rand_frac()
{
	//if not yet seeded, then seed
	if(!g_rand_seeded)
	{
		srand((unsigned int)time(NULL));
		g_rand_seeded=true;
	}
	return ((double)rand()+1)/((double)RAND_MAX+2);
}

//uniformly creates a random number uniformly distributed between 2 values, non inclusive
template <class T> const T rand_val(const T lower, const T upper)
{
	return (T)((rand_frac()*(upper-lower))+lower);
}


//global copy of publisher
ros::Publisher pub;

//convert from amcl output pose to gps and republish
void callback(const geometry_msgs::PoseWithCovarianceStamped& tf)
{
	//set up output message
	sensor_msgs::NavSatFix gps_data;
    gps_data.header.frame_id="odom";
    gps_data.header.stamp = tf.header.stamp;
    gps_data.status.status = sensor_msgs::NavSatStatus::STATUS_FIX;
    gps_data.status.service = sensor_msgs::NavSatStatus::SERVICE_GPS;
    gps_data.position_covariance = {1, 0, 0, 0, 1, 0, 0, 0, 1};
    gps_data.position_covariance_type = gps_data.COVARIANCE_TYPE_UNKNOWN;
	
	//add noise
	double noise_range = 0.1;
	double longi = tf.pose.pose.position.y/100.0  + 1.0 + rand_val<double>(-noise_range, noise_range);
	double lati = tf.pose.pose.position.x/100.0 + 1.0 + rand_val<double>(-noise_range, noise_range);


    //now use the input transform object to fill in the longitude and latitude - This is the dodgy hacky part
    /*RobotLocalization::NavsatConversions::UTMtoLL(longi, lati, "U", gps_data.latitude, gps_data.longitude);
    */
    gps_data.latitude = lati;
    gps_data.longitude = longi;
    gps_data.altitude = tf.pose.pose.position.z;

    pub.publish(gps_data);
}

int main(int argc, char** argv)
{
	try
	{
		ros::init(argc, argv, "amcl_gps_faker");
		ros::NodeHandle n;

		//subscribe to vicon transforms
		ros::Subscriber sub = n.subscribe("/amcl_pose", 10, &callback);

		//set up publisher for gps data
		pub = n.advertise<sensor_msgs::NavSatFix>("/gps/fix", 10);

		ros::spin();

		return 0;
	}
	catch(exception& e)
	{
		cerr << "Exception thrown:" << e.what() << endl;
	}
	catch(...)
	{
		cerr << "Unknown exception thrown" << endl;
	}
	return 1;
}
