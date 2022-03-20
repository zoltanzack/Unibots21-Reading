import cv2
import numpy as np
import math

class Camera:
    """Wrapper class for camera"""
    
    def __init__(self, size=(720,420)):
        # Get camera object reference
        self.camera = None
        
        # TEMP
        self.frame = cv2.imread('../apriltags/test_environment_2.png', 1)
        size = 720
        ratio = self.frame.shape[1] / self.frame.shape[0]   
        self.frame = cv2.resize(self.frame, (int(size * ratio), size), interpolation=cv2.INTER_AREA)
        
    def getFrame(self):
        # Get frame
        # Scale frame using self.size
        # Return frame from camera
        return self.frame

class Vision: # All is subject to optimisation if possible. This was quickly put together to get the vision tasks operating so the robot can be tested and developed

    class Options:
        GRAY = 0
        COLOUR = 1
        HSV = 2

    directionColours = [(0, 255, 255), (255, 0, 200), (0, 127, 255), (0, 230, 0)] # Yellow, Purple, Orange, Green
    exactBallColours = [(40, 215, 200), (80, 190, 255)]
    compassDirections = ['E', 'ENE', 'NE', 'NNE', 'N', 'NNW', 'NW', 'WNW', 'W', 'WSW', 'SW', 'SSW', 'S', 'SSE', 'SE', 'ESE']
    aprilTag_definition = np.array([[1,1,1,1,1,1,1,1,1,1],
                                    [1,0,0,0,0,0,0,0,0,1],
                                    [1,0,0,0,0,0,0,0,0,1],
                                    [1,0,0,0,0,0,0,0,0,1],
                                    [1,0,0,0,0,0,0,0,0,1],
                                    [1,0,0,0,0,0,0,0,0,1],
                                    [1,0,0,0,0,0,0,0,0,1],
                                    [1,0,0,0,0,0,0,0,0,1],
                                    [1,0,0,0,0,0,0,0,0,1],
                                    [1,1,1,1,1,1,1,1,1,1]])
        
    # Member variables to be populated through the computer vision (CV) tasks
    frame = None # Current frame taken from the camera to be used during CV tasks
    virtualisedView = None # The virtualised view used for viewing the processing of the robot's vision tasks
    direction = None # Estimated direction the robot is facing
    floor_mask = None # Binary image representing the floor region in the frame
    wall_mask = None # Binary image representing the visible (for now; could potentially extrapolate occluded sections) walls in the frame
    
    def __init__(self, wallColourRanges, tennis_ball_colour, ping_pong_colour, produceVirtualisation = True):
        self.wallColours = wallColourRanges
        self.tennis_ball_colour = tennis_ball_colour
        self.ping_pong_colour = ping_pong_colour
        
        self.produceVirtualisation = produceVirtualisation
    
    def update(self, frame):
        """ 
        Updates the frame using for CV tasks
        *Must be called before any other method for correct operation*
        """
        self.frame = frame
        
        # Not really needed but, hey-ho
        self.virtualisedView = None
        self.direction = None
        self.floor_mask = None
        self.wall_mask = None 
    
    def calculateOrientation(self): # First ("prerequisite") task for any other task
        """
        Calculates the robot's (rough) orientation
        Makes new virtualised view for this frame
        """
        # Calculate orientation
        walls_image, self.wall_mask, walls = self.__detectWalls()
        self.direction = self.__calculateDirection(walls)

        # Produce virtualisation
        if self.produceVirtualisation:
            self.virtualisedView = walls_image.copy()
            cv2.putText(self.virtualisedView, self.__createDirectionName(self.direction), (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 255, 255), 2, cv2.LINE_AA)
          
        # Create floor mask 
        
        # rescale wall_mask to very small size
        print(self.wall_mask.shape)
        test = cv2.dilate(self.wall_mask, np.ones((2,2)), 1)
        test = cv2.resize(test, None, fx=0.1, fy=0.1)
        #cv2.imshow("Shrank wall mask", test)
        
        # detect 
        
        temp_mask = self.wall_mask.copy()
        temp_mask = cv2.dilate(temp_mask, np.ones((2,2)), 1)
        temp_mask = ~temp_mask
        temp_mask[temp_mask!=0] = 255
        cv2.imshow("floor mask", temp_mask)
        contours, _ = cv2.findContours(temp_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        self.floor_mask = np.zeros_like(temp_mask)
        cv2.fillPoly(self.floor_mask, pts=[contours[0]], color=255)
        
        # Add floor to virtualisation
        if self.produceVirtualisation:
            cv2.fillPoly(self.virtualisedView, pts=[contours[0]], color=(220, 220, 220))
           
    # Refactor
    def identifyBalls(self):
        # Get floor region
        masked_balls = self.frame.copy()
        masked_balls[self.floor_mask==0] = 0
        
        # Detect circles 
        # Maybe blur if needed
        circles = cv2.HoughCircles(self.__convertColour(masked_balls, self.Options.GRAY), cv2.HOUGH_GRADIENT, 1, 30, param1=60, param2=30, minRadius=0, maxRadius=0)
        circles = np.uint16(np.around(circles))[0]
        
        balls_hsv = self.__convertColour(masked_balls, self.Options.HSV)
        tennis_balls = []
        ping_pong_balls = []
        for c in circles:
            if self.__colourInRange(balls_hsv, (c[1],c[0]), self.tennis_ball_colour):
                tennis_balls.append(c)
            elif self.__colourInRange(balls_hsv, (c[1],c[0]), self.ping_pong_colour):
                ping_pong_balls.append(c)
                
            cv2.circle(masked_balls, (c[0],c[1]), c[2], (0,255,0), 2) # draw the outer circle
            cv2.circle(masked_balls, (c[0],c[1]), 2, (0,0,255), 3) # draw the center of the circle
        
        if self.produceVirtualisation:
            for ball in tennis_balls:
                cv2.circle(self.virtualisedView, (ball[0],ball[1]), ball[2], self.exactBallColours[0], -1)
            for ball in ping_pong_balls:
                cv2.circle(self.virtualisedView, (ball[0],ball[1]), ball[2], self.exactBallColours[1], -1)
        
    def identifyFiducials(self):
        # Form search area
        tag_search_image = self.frame.copy()
        tag_search_image[self.wall_mask==0] = (0, 0, 0)
        #cv2.imshow("tag search", tag_search_image)

        # 3.2 Threshold april tag colours
        tag_search_hsv = self.__convertColour(tag_search_image, self.Options.HSV)
        tag_image = self.__colourExtract(tag_search_hsv, ((0, 0, 10), (255, 47, 255)))
        tags_masked = tag_search_image.copy()
        tags_masked[tag_image==0] = (0, 0, 0)
        #cv2.imshow("tag thresh", tag_image)

        # 3.3 Contour tags to segregate them
        tag_contours, _ = cv2.findContours(tag_image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        tags = []
        # 3.4 Perform perspective transformation            
        for tag in tag_contours:
            if cv2.contourArea(tag) < 50:
                continue
        
            contour_image = np.zeros_like(tags_masked)
            cv2.drawContours(contour_image, [tag], -1, 255, -1)
            moments = cv2.moments(self.__convertColour(contour_image, self.Options.GRAY))
            center = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"])) # Image moments, puzzling stuff
            #cv2.putText(tags_masked, str(i), center, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

            pts1 = self.__getFurthestFourPoints(tag, center)
            if pts1 is None:
                continue
            
            #cv2.circle(tags_masked, pts1[0], 4, (0, 0, 255), -1)
            #cv2.circle(tags_masked, pts1[1], 4, (0, 255, 0), -1)
            #cv2.circle(tags_masked, pts1[2], 4, (255, 0, 0), -1)
            #cv2.circle(tags_masked, pts1[3], 4, (0, 255, 255), -1)

            pts2 = np.float32([[0,0],[0,320],[320,320],[320,0]])        
            matrix = cv2.getPerspectiveTransform(pts1.astype(np.float32), pts2)
            tags.append(((cv2.boundingRect(tag)), cv2.warpPerspective(tags_masked, matrix, (320, 320), flags=cv2.INTER_NEAREST))) # ((x,y,w,h), image)

        #cv2.imshow("tag masked", tags_masked)
        
        #for i, tag in enumerate(tags): 
        #    cv2.imshow(f'tag {i}', tag[1])

        # 3.3 Create apriltag matrix
        tag_mats = []
        temp_tags = []
        for i in range(len(tags)):
            tag_mat = np.ones([10,10], dtype=np.uint8)
            
            image = self.__convertColour(tags[i][1], self.Options.GRAY)
            #cv2.imshow(f'tags 0 {i}', image)
            _, thresh = cv2.threshold(image, 70, 255, cv2.THRESH_BINARY)

            for y in range(10):
                for x in range(10):
                    point = (y*32+16, x*32+16)
                    tag_mat[y,x] = 1 if thresh[point[0],point[1]] else 0
                    #cv2.circle(thresh, (point[1], point[0]), 2, 127, -1)
            
            # Verify is april tag
            if np.array_equal(np.bitwise_and(tag_mat, self.aprilTag_definition), self.aprilTag_definition):
                tag_mats.append(tag_mat)
                temp_tags.append(tags[i])
            
            #cv2.imshow(f'tags {i}', thresh)
        tags = temp_tags
        print(f'Found {len(tags)} april tags')
        
        # Reproduce apriltag - testing
        tag_mat_images = []
        for i in range(len(tags)):
            tag_mat_images.append(np.empty((320,320), dtype=np.uint8))
            for y in range(tag_mats[i].shape[0]):
                for x in range(tag_mats[i].shape[1]):
                    tag_mat_images[i][y*32:y*32+32, x*32:x*32+32] = 255 if tag_mats[i][y,x] else 0
 
            #cv2.imshow(f'reproduced tag {i}', tag_mat_images[i])

        # Overlay reproduced april tags onto virtualisation image
        if self.produceVirtualisation:
            for i in range(len(tags)):
                x,y,w,h = tags[i][0] # alias
                self.virtualisedView[y:y+h,x:x+h] = cv2.resize(self.__convertColour(tag_mat_images[i], self.Options.COLOUR), (h,h), interpolation=cv2.INTER_NEAREST)
            
    def getVirtualisedView(self):
        return self.virtualisedView

    # Private methods for computer vision tasks
    def __detectWalls(self):
        wall_image = np.zeros_like(self.frame)
        wall_mask = np.zeros((wall_image.shape[0], wall_image.shape[1]), dtype=np.uint8)
        walls = []
        for direction, wall in enumerate(self.wallColours): # Loop through walls
            mask = self.__colourExtract(self.frame, wall, convert=True)
            contours, _ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            contours = [contour for contour in contours if cv2.contourArea(contour) > 5000]

            if len(contours) > 0:
                contour_mask = np.zeros_like(wall_mask)
                cv2.fillPoly(contour_mask, pts=contours, color=255)
                moments = cv2.moments(contour_mask)
                center = (int(moments["m10"] / moments["m00"]), int(moments["m01"] / moments["m00"])) # Image moments, puzzling stuff
                points = self.__getFurthestFourPoints(contours, center, multi=True)
                contour_array = np.array([points])
                
                cv2.circle(wall_image, points[0], 4, (0, 0, 255), -1)
                cv2.circle(wall_image, points[1], 4, (0, 255, 0), -1)
                cv2.circle(wall_image, points[2], 4, (255, 0, 0), -1)
                cv2.circle(wall_image, points[3], 4, (0, 255, 255), -1)
                
                cv2.fillPoly(wall_image, pts=contour_array, color=self.directionColours[direction])
                cv2.fillPoly(wall_mask, pts=contour_array, color=255)
     
                walls.append((direction, contour_array))

        return wall_image, wall_mask, walls
    
    def __getFurthestFourPoints(self, points, center, multi=False):
        if multi: # Convert list of contours into single list of multiple contours
            points = [point for contour in points for point in contour]
    
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
                
        for i in range(len(furthest)):
            if furthest[i] is None:
                return None
                
        return np.array(furthest)
    
    def __updateDirectionList(self, list, newVal, pos = 0):             
        old = newVal
        if newVal[0] > list[pos][0]:
            old = list[pos]
            list[pos] = newVal
            
        if pos == len(list)-1: 
            return list
        else:
            return self.__updateDirectionList(list, old, pos+1)
            
    def __createDirectionName(self, direction):
        angle = math.atan2(direction[0], direction[1])
        compass_index = int(16 * angle / (2*math.pi) + 16) % 16
        return self.compassDirections[compass_index]

    def __calculateDirection(self, walls):
        """ Creates (y,x) vector of the estimated forward direction of the robot """
        largest = [(-1, None), (-1, None), (-1, None), (-1, None)] # (Area, Wall)
        count = len(largest)
        for wall in walls:
            largest = self.__updateDirectionList(largest, (cv2.contourArea(wall[1]), wall))
        
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
    
    def __convertColour(self, image, colour_mode): # Yeah, i know wrong way round, but, i'll vibe with it for now
        if colour_mode == self.Options.GRAY:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        elif colour_mode == self.Options.COLOUR:
            return cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
        elif colour_mode == self.Options.HSV:
            if image.shape[2] != 3:
                cv2.cvtColor(cv2.cvtColor(image, cv2.COLOR_GRAY2BGR))
            return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        else:
            return image
    
    def __colourExtract(self, image, range, convert=False):
        hsv = image
        if convert:
            hsv = self.__convertColour(image, self.Options.HSV)
        return cv2.inRange(hsv, range[0], range[1])
    
    def __colourInRange(self, image, coordinate, range, convert=False):
        hsv = image
        if convert:
            hsv = self.__convertColour(image, self.Options.HSV)
        return np.all(np.greater(image[coordinate], range[0])) and np.all(np.less(image[coordinate], range[1]))
        
    def __edgeDetect(self, image, colour_mode = Options.COLOUR):
        source = image.copy()
        if colour_mode != None:
            source = self.__convertColour(source, colour_mode)
        sobel_edge_x = cv2.Sobel(src=source, ddepth=cv2.CV_64F, dx=1, dy=0)
        sobel_edge_y = cv2.Sobel(src=source, ddepth=cv2.CV_64F, dx=0, dy=1)
        sobel_edge_x = cv2.convertScaleAbs(sobel_edge_x)
        sobel_edge_y = cv2.convertScaleAbs(sobel_edge_y)
        sobel_edge_xy = cv2.addWeighted(sobel_edge_x, 0.5, sobel_edge_y, 0.5, 0)
        _, sobel_edge_xy = cv2.threshold(sobel_edge_xy, 21, 255, cv2.THRESH_BINARY)
        
        return sobel_edge_xy

if __name__ == "__main__":
    test_image = cv2.imread('../../apriltags/test_environment_6.png', 1)


    size = 720
    ratio = test_image.shape[1] / test_image.shape[0]   
    test_image = cv2.resize(test_image, (int(size * ratio), size))

    test_image_gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        
    cv2.imshow("test_image", test_image)

    wallColours = [
        ((24, 113, 174), (27, 156, 210)), # Yellow - North
        ((160, 190, 132), (165, 227, 154)), # Purple - East
        ((4, 144, 111), (20, 217, 198)), # Orange - South
        ((49, 125, 97), (74, 227, 196)) # Green - West
    ]

    #tennis_ball_colour = ((30, 56, 45), (39, 248, 193)) # - From live camera (strict)
    #tennis_ball_colour = ((10, 47, 85), (41, 239, 210)) # - From test environment (lenient)
    tennis_ball_colour = ((30, 50, 90), (50, 255, 255)) # - For hough circle transform (very lenient)
    #ping_pong_colour = ((98, 53, 107), (162, 106, 169)) # - From live camera
    #ping_pong_colour = ((5, 0, 122), (100, 22, 216)) # - From test environment (lenient)
    #ping_pong_colour = ((8, 0, 122), (100, 18, 202)) # - From test environment (strict)
    ping_pong_colour = ((0, 0, 100), (255, 30, 255)) # - For hough circle transform (very lenient)
    
    floor_colour = ((105, 0, 206), (121, 16, 255))

    vision = Vision(wallColours, tennis_ball_colour, ping_pong_colour, floor_colour)
    vision.update(test_image)
    vision.calculateOrientation()
    vision.identifyBalls()
    vision.identifyFiducials()
    
    cv2.imshow("Virtualisation", vision.getVirtualisedView())

    cv2.waitKey(0)

