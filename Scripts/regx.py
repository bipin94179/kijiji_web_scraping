import re

html = '''
<div class="search-item regular-ad" data-listing-id="1508838784" data-vip-url="/v-commercial-office-space/calgary/clinic-treatment-room-for-rent/1508838784">
<div class="clearfix">
<div class="left-col">
<div class="fes-favourite">
<div class="fes-pagelet">
<div data-fes-id="favouriteButton1508838784"><div class="loginToFavourite-841062542"><div class="buttonWrapper-2469744582"><button class="favouriteButton-2394815451 favouriteButton__default-3002028217 favouriteButton-3214127281" data-testid="favourite-button" title="Click to add to My Favourites" type="button"><svg class="icon-459822882 favouriteButtonIcon__default-1548764540 filled favouriteButtonIcon-4183586163" focusable="false" height="100%" role="img" width="100%"><use xlink:href="#icon-heart"></use></svg><span class="favouriteButtonLabel-2715849804 favouriteButtonLabel__default-2722470893">Favourite</span></button></div></div></div>
<script type="text/javascript">if(rehydrate===undefined){var rehydrate={};}rehydrate["favouriteButton1508838784"]={componentPath:"Shared/FavouriteButtonSmall",props:{"isLoginToFavourite":true,"adId":1508838784,"adSource":"O","filled":true}};</script>
</div>
</div>
<div class="image">
<picture>
<source alt="Clinic/treatment room for rent" data-srcset="https://i.ebayimg.com/images/g/gsgAAOSw-m1e9v~f/s-l200.webp" srcset="https://ca.classistatic.com/static/V/9383/img/placeholder-large.png" type="image/webp"/>
<img alt="Clinic/treatment room for rent" data-src="https://i.ebayimg.com/images/g/gsgAAOSw-m1e9v~f/s-l200.jpg" src="https://ca.classistatic.com/static/V/9383/img/placeholder-large.png"/>
</picture>
</div>
</div>
<div class="info">
<div class="info-container">
<div class="price">
                        
                            
                            
                                
                                
                                    $850.00
                                    
                                    
                                    
                                
                                
                            
                            

                            
                                
                                
                            
                        
                    </div>
<div class="title">
<a class="title" href="/v-commercial-office-space/calgary/clinic-treatment-room-for-rent/1508838784">
                            Clinic/treatment room for rent
                        </a>
</div>
<div class="distance">
</div>
<div class="location">
<span class="">
                            
                            Calgary
                          </span>
<span class="date-posted">&lt; 60 minutes ago</span>
</div>
<div class="description">
                        Clean, quiet treatment room for rent full-time in professional building in Capitol Hill NW. Partially furnished with cabinet and desk. Room has its own sink (key for AHS approval). Located across ...
                        
                            
                            
                            
                        

                        

                        <div class="details">
</div>
</div>
</div>
</div>
</div>
'''

x = re.search('<a class="title" href=+["-/a-zA-Z0-9]*>{1}', html)

print(x)
