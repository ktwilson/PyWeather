class Constants(object):
    trends = {
          196:'Falling Rapidly',
		  236:'Falling Slowly',
		  0:'Steady',
		  20:'Rising Slowly',
		  60:'Rising Rapidly'
		}

    directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW', 'N']


    forecasts = {
            1: '/weather/forecastimages/rain.gif',
            2: '/weather/forecastimages/cloudy.gif',
            3: '/weather/forecastimages/rain.gif',
            4: '/weather/forecastimages/partlycloudy.gif',
            6: '/weather/forecastimages/partlycloudy.gif',
             7: '/weather/forecastimages/partlycloudyandrain.gif',       
             8:  '/weather/forecastimages/sunny.gif',
             16: '/weather/forecastimages/snow.gif',
             18: '/weather/forecastimages/snow.gif',                
             19: '/weather/forecastimages/snowandrain.gif',                
             22: '/weather/forecastimages/partlycloudyandsnow.gif',                
             23: '/weather/forecastimages/partlycloudyandsnow.gif'                
            } 