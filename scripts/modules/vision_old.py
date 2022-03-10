import cv2
import numpy as np
import math

class Vision:
    class Options:
        GRAY = 0
        COLOUR = 1
        HSV = 2

    def __init__(self, wallColourRanges):
        self.wallColours = wallColourRanges
        
        wallColours = [
            ((24, 113, 174), (27, 156, 210)), # Yellow - North
            ((160, 190, 132), (165, 227, 154)), # Purple - East
            ((4, 144, 111), (20, 217, 198)), # Orange - South
            ((49, 125, 97), (74, 227, 196)) # Green - West
        ]

    def __convertColour(self, image, colour_mode): # Yeah, i know wrong way round, but, i'll vibe with it for now
        if colour_mode == Options.GRAY:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        elif colour_mode == Options.COLOUR:
            return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        elif colour_mode == Options.HSV:
            if image.shape[2] != 3:
                cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR))
            return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        else:
            return image

    def __edgeDetect(self, image, colour_mode = Options.COLOUR):
        source = image.copy()
        if colour_mode != None:
            source = convertColour(source, colour_mode)
        sobel_edge_x = cv2.Sobel(src=source, ddepth=cv2.CV_64F, dx=1, dy=0)
        sobel_edge_y = cv2.Sobel(src=source, ddepth=cv2.CV_64F, dx=0, dy=1)
        sobel_edge_x = cv2.convertScaleAbs(sobel_edge_x)
        sobel_edge_y = cv2.convertScaleAbs(sobel_edge_y)
        sobel_edge_xy = cv2.addWeighted(sobel_edge_x, 0.5, sobel_edge_y, 0.5, 0)
        _, sobel_edge_xy = cv2.threshold(sobel_edge_xy, 21, 255, cv2.THRESH_BINARY)
        
        #cv2.imshow("edge x", sobel_edge_x)
        #cv2.imshow("edge y", sobel_edge_y)
        
        return sobel_edge_xy

    def __colourExtract(image, lower, upper, colour_mode = None):
        source = image.copy()
        if colour_mode != None:
            source = convertColour(source, colour_mode)
        hsv = convertColour(source, Options.HSV)
        return cv2.inRange(hsv, lower, upper)



directionColours = [(0, 255, 255), (255, 0, 200), (0, 127, 255), (0, 230, 0)]

def detectWalls(image):
    wall_image = np.zeros_like(image)
    wall_mask = np.zeros((wall_image.shape[0], wall_image.shape[1]), dtype=np.uint8)
    walls = []
    for direction, wall in enumerate(wallColours): # Loop through walls
        mask = colourExtract(image, wall[0], wall[1])
        contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for contour in contours:
            print(cv2.contourArea(contour))
            if cv2.contourArea(contour) > 8000:
                walls.append((direction, contour))
                #cv2.drawContours(wall_image, contours, -1, (0, 255, 0), 3, cv2.LINE_AA)
                cv2.fillPoly(wall_image, pts=[contour], color=directionColours[direction])
                cv2.fillPoly(wall_mask, pts=[contour], color=255)

    return wall_image, wall_mask, walls

def updateDirectionList(list, newVal, pos = 0):             
    old = newVal
    if newVal[0] > list[pos][0]:
        old = list[pos]
        list[pos] = newVal
        
    if pos == len(list)-1: 
        return list
    else:
        return updateDirectionList(list, old, pos+1)

compassDirections = ['E', 'ENE', 'NE', 'NNE', 'N', 'NNW', 'NW', 'WNW', 'W', 'WSW', 'SW', 'SSW', 'S', 'SSE', 'SE', 'ESE']

def createDirectionName(direction):
    angle = math.atan2(direction[0], direction[1])
    compass_index = int(16 * angle / (2*math.pi) + 16) % 16
    return compassDirections[compass_index]

def calculateDirection(walls):
    largest = [(-1, None), (-1, None), (-1, None), (-1, None)] # (Area, Wall)
    count = len(largest)
    for wall in walls:
        largest = updateDirectionList(largest, (cv2.contourArea(wall[1]), wall))
    
    forward = 0
    right = 0
    for wall in largest:
        if wall[1] is None:
            break
        #print(wall[0], wall[1][0])
        if wall[1][0] == 0: # North
            forward += wall[0] # Add area
        elif wall[1][0] == 1: # East
            right += wall[0] 
        elif wall[1][0] == 2: # South
            forward -= wall[0] 
        elif wall[1][0] == 3: # West
            right -= wall[0]
    
    total = abs(forward) + abs(right)
    return (forward/total, right/total)
    
# ------------------------------------------------------------------------------- #
      
#test_image = cv2.imread('../../apriltags/tag36_11_00032.png', 1)
#new_size = (test_image.shape[0] * 32, test_image.shape[1] * 32)
#test_image = cv2.resize(test_image, new_size, interpolation = cv2.INTER_NEAREST)

test_image = cv2.imread('../../apriltags/test_environment_2.png', 1)

size = 720
ratio = test_image.shape[1] / test_image.shape[0]   
test_image = cv2.resize(test_image, (int(size * ratio), size))

test_image_gray = convertColour(test_image, Options.GRAY)
    
cv2.imshow("test_image", test_image)
    
# 1 Orient self
walls_image, wall_mask, walls = detectWalls(test_image)
direction = calculateDirection(walls)

# Produce virtualisation
virtualised_image = walls_image.copy()
cv2.putText(virtualised_image, createDirectionName(direction), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 2, cv2.LINE_AA)
  
# Add floor to virtualisation
temp_mask = wall_mask.copy()
temp_mask = cv2.dilate(temp_mask, np.ones((5,5)), 1)
temp_mask = ~temp_mask
temp_mask[temp_mask!=0] = 255
contours, _ = cv2.findContours(temp_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
ball_mask = np.zeros_like(temp_mask)
cv2.fillPoly(ball_mask, pts=[contours[0]], color=(255, 255, 255))
cv2.fillPoly(virtualised_image, pts=[contours[0]], color=(220, 220, 220))

# 2 Detect balls
if True:
    masked_balls = test_image.copy()
    masked_balls[ball_mask==0] = 0
    cv2.imshow("ball mask", masked_balls)

    # Ball masks
    tennis_balls_mask = colourExtract(test_image, (30, 56, 45), (39, 248, 193)) # - From live camera (strict)
    #tennis_balls_mask = colourExtract(test_image, (10, 47, 85), (41, 239, 210)) # - From test environment (lenient)
    #ping_pong_mask = colourExtract(test_image, (98, 53, 107), (162, 106, 169)) # - From live camera
    #ping_pong_mask = colourExtract(test_image, (5, 0, 122), (100, 22, 216)) # - From test environment (lenient)
    ping_pong_mask = colourExtract(test_image, (8, 0, 122), (100, 18, 202)) # - From test environment (strict)

    # Ball mask contours
    tennis_balls_contours, _ = cv2.findContours(tennis_balls_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    ping_pong_contours,    _ = cv2.findContours(ping_pong_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Ball contours
    contour_list = []
    for contour in tennis_balls_contours + ping_pong_contours:
        if cv2.contourArea(contour) > 1000: # Make this proportional to frame size
            contour_list.append(contour)
            
    balls = convertColour(tennis_balls_mask, Options.COLOUR) + convertColour(ping_pong_mask, Options.COLOUR)
    cv2.drawContours(balls, contour_list, -1, (0, 255, 0), 2, cv2.LINE_AA)
    cv2.imshow("Balls", balls)

# 3 Detect apriltag
# 3.1 Form search area
tag_search_image = test_image.copy()
tag_search_image[wall_mask==0] = (0, 0, 0)
#cv2.imshow("tag search", tag_search_image)

# 3.2 Threshold april tag colours
tag_search_hsv = convertColour(tag_search_image, Options.HSV)
tag_image = cv2.inRange(tag_search_hsv, (0, 0, 10), (255, 47, 255))
tags_masked = tag_search_image.copy()
tags_masked[tag_image==0] = (0, 0, 0)
#cv2.imshow("tag thresh", tag_image)

# 3.3 Contour tags to segregate them
test = convertColour(tag_image, Options.COLOUR)
tag_contours, _ = cv2.findContours(tag_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
tags = []
print(f'Can see {len(tag_contours)} april tags')

# 3.4 Perform perspective transformation 
def getFurthestFourPoints(points, center):
    furthest = [None, None, None, None]
    for point in points:
        point = point[0]
        distance = (point[0]-center[0], point[1]-center[1])
        direction  = 2 if distance[0] > 0 else 0 # x (left-right)
        if direction != 2: # top-right is (1,-1) not (1,1) so can't repeat above line for y (up-down)
            direction += 1 if distance[1] > 0 else 0
        else:
            direction += 1 if distance[1] < 0 else 0        
        
        furthestDist = furthestDistance = 0
        if furthest[direction] is not None:
            furthestDistance = (furthest[direction][0]-center[0], furthest[direction][1]-center[1])
            furthestDist = math.sqrt(abs(furthestDistance[0])+abs(furthestDistance[1]))
            
        newDist = math.sqrt(abs(distance[0])+abs(distance[1]))
        
        #print(furthest[direction], point, direction, "|", distance, newDist, furthestDistance, furthestDist)
        
        if furthestDist < newDist:
            furthest[direction] = point
            
    return np.array(furthest)
     
for tag in tag_contours:
    contour_image = np.zeros_like(tags_masked)
    cv2.drawContours(contour_image, [tag], -1, 255, -1)
    moments = cv2.moments(convertColour(contour_image, Options.GRAY))
    center = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"])) # Image moments, puzzling stuff
    #cv2.putText(tags_masked, str(i), center, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    
    pts1 = getFurthestFourPoints(tag, center)
    
    
    #cv2.circle(tags_masked, pts1[0], 4, (0, 0, 255), -1)
    #cv2.circle(tags_masked, pts1[1], 4, (0, 255, 0), -1)
    #cv2.circle(tags_masked, pts1[2], 4, (255, 0, 0), -1)
    #cv2.circle(tags_masked, pts1[3], 4, (0, 255, 255), -1)

    pts2 = np.float32([[0,0],[0,320],[320,320],[320,0]])        
    matrix = cv2.getPerspectiveTransform(pts1.astype(np.float32), pts2)
    tags.append(((cv2.boundingRect(tag)), cv2.warpPerspective(tags_masked, matrix, (320, 320), flags=cv2.INTER_NEAREST))) # ((x,y,w,h), image)

#cv2.imshow("tag masked", tags_masked)
#for i, tag in enumerate(tags): 
#    cv2.imshow(f'tag {i}', tag)

# 3.3 Create apriltag matrix
tag_mats = []
for i in range(len(tags)):
    tag_mats.append(np.ones([10,10]))
    
    image = convertColour(tags[i][1], Options.GRAY)
    #cv2.imshow(f'tags 0 {i}', image)
    _, thresh = cv2.threshold(image, 70, 255, cv2.THRESH_BINARY)

    for y in range(10):
        for x in range(10):
            point = (y*32+16, x*32+16)
            tag_mats[i][y,x] = thresh[point[0],point[1]]
            #cv2.circle(thresh, point, 2, 127, -1)

    #cv2.imshow(f'tags {i}', thresh)

# Reproduce apriltag - testing
tag_mat_images = []
for i in range(len(tags)):
    tag_mat_images.append(np.empty((320,320), dtype=np.uint8))
    for y in range(tag_mats[i].shape[0]):
        for x in range(tag_mats[i].shape[1]):
            tag_mat_images[i][y*32:y*32+32, x*32:x*32+32] = 255 if tag_mats[i][y,x] else 0

    cv2.imshow(f'reproduced tag {i}', tag_mat_images[i])

# Overlay reproduced april tags onto virtualisation image
if True:
    for i in range(len(tags)):
        x,y,w,h = tags[i][0] # alias
        virtualised_image[y:y+h,x:x+h] = cv2.resize(convertColour(tag_mat_images[i], Options.COLOUR), (h,h), interpolation=cv2.INTER_NEAREST)
    
cv2.imshow("Virtualisation", virtualised_image)

cv2.waitKey(0)

