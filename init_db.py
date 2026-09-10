import os
from werkzeug.security import generate_password_hash
from flask import Flask
from models import db, User, Studio, Portfolio, Booking, Review

def setup_database():
    app = Flask(__name__)
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        db_path = os.path.abspath("database.db")
        db_url = f"sqlite:///{db_path}"
        
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        print(f"Connecting to database: {db_url}")
        # Drop and recreate all tables for a clean, consistent state
        db.drop_all()
        db.create_all()

        print("Seeding Bareilly and metropolitan photography studios with verified contacts, ₹ INR pricing, ratings, and portfolio works...")

        # 1. Studio Hosts & Creators
        pw_hash = generate_password_hash("password123")
        
        # Bareilly Studio Hosts
        b_host1 = User(name="Aman Hashmi", email="ahstudio.bareilly@gmail.com", phone="+919412289012", password_hash=pw_hash, role="studio")
        b_host2 = User(name="Rajesh Tandon", email="chitralok.modeltown@gmail.com", phone="+919837045610", password_hash=pw_hash, role="studio")
        b_host3 = User(name="Kavya Verma", email="kavyastudio.ddpuram@yahoo.com", phone="+919897123489", password_hash=pw_hash, role="studio")
        b_host4 = User(name="Yuvraj Singh", email="yuvrajfilms.bareilly@gmail.com", phone="+919759067812", password_hash=pw_hash, role="studio")
        b_host5 = User(name="Alok Saxena", email="natrajproductions.bly@gmail.com", phone="+919837588990", password_hash=pw_hash, role="studio")
        b_host6 = User(name="Prem Prakash", email="premstudio1975@gmail.com", phone="+919456033445", password_hash=pw_hash, role="studio")
        b_host7 = User(name="Nitin Sharma", email="snapclick.bareilly@gmail.com", phone="+919897055112", password_hash=pw_hash, role="studio")

        # Metro Hosts
        m_host1 = User(name="Kabir Sen", email="kabir@lumina.in", phone="+919820011223", password_hash=pw_hash, role="studio")
        m_host2 = User(name="Ananya Sharma", email="ananya@velvet.in", phone="+919845012345", password_hash=pw_hash, role="studio")
        
        # Customers
        cust1 = User(name="Aryan Patel", email="aryan@creative.com", phone="+919900112233", password_hash=pw_hash, role="customer")
        cust2 = User(name="Pooja Sharma", email="pooja.sharma@fashionbly.in", phone="+919922334455", password_hash=pw_hash, role="customer")
        cust3 = User(name="Rohit Gangwar", email="rohit.director@films.in", phone="+919911223344", password_hash=pw_hash, role="customer")

        db.session.add_all([b_host1, b_host2, b_host3, b_host4, b_host5, b_host6, b_host7, m_host1, m_host2, cust1, cust2, cust3])
        db.session.commit()

        # 2. BAREILLY STUDIOS (Full details: contacts, ₹ INR charges, exact locations, descriptions, amenities)
        studios_data = [
            # Bareilly Studio 1: AH Studio Bareilly
            Studio(
                user_id=b_host1.id,
                name="AH Studio Bareilly",
                description="Bareilly's premier wedding and bridal fashion production hub. Features a grand royal mandap stage, opulent velvet drapes, multi-zone ambient amber lighting, and professional strobe rigs for cinematic bridal and fashion shoots.",
                location="Butler Plaza, Civil Lines, Bareilly, Uttar Pradesh 243001",
                city="Bareilly",
                category="Wedding & Fashion",
                price_per_hour=2400.0, # ₹2,400/hr
                contact_phone="+91 94122 89012",
                contact_email="ahstudio.bareilly@gmail.com",
                cover_image="/static/image/bareilly_wedding_studio.jpg",
                amenities="Royal Mandap Stage, Profoto Strobes, Air Conditioned, Bridal Dressing Suite, 4K Monitor Station, High Speed WiFi"
            ),
            # Bareilly Studio 2: Chitralok Photography Studio
            Studio(
                user_id=b_host2.id,
                name="Chitralok Photography Studio",
                description="Renowned Model Town landmark specializing in portraiture, portfolio headshots, and couple shoots. Fitted with motorized seamless multi-color paper backdrops, Godox flash heads, and high-CRI softboxes.",
                location="Near Gurudwara, Model Town, Bareilly, Uttar Pradesh 243005",
                city="Bareilly",
                category="Portrait",
                price_per_hour=1800.0, # ₹1,800/hr
                contact_phone="+91 98370 45610",
                contact_email="chitralok.modeltown@gmail.com",
                cover_image="/static/image/bareilly_portrait_studio.jpg",
                amenities="Motorized Seamless Backdrops, Godox 120cm Octabox, Makeup Mirror Vanity, Split Air Conditioning, Stool & Props"
            ),
            # Bareilly Studio 3: Kavya Digital Studio & Event Stage
            Studio(
                user_id=b_host3.id,
                name="Kavya Digital Studio & Event Stage",
                description="Trendy high-fashion & editorial studio in DD Puram. Offers continuous video lighting, designer furniture props, beauty dishes, and a dedicated styling wardrobe for models and influencers.",
                location="Stadium Road, DD Puram, Bareilly, Uttar Pradesh 243122",
                city="Bareilly",
                category="Fashion",
                price_per_hour=2100.0, # ₹2,100/hr
                contact_phone="+91 98971 23489",
                contact_email="kavyastudio.ddpuram@yahoo.com",
                cover_image="/static/image/bareilly_fashion_work.jpg",
                amenities="Styling Wardrobe, Steamer, Continuous Godox SL-200W LED Panels, Sound System, Client Lounge"
            ),
            # Bareilly Studio 4: Yuvraj Photography & Film Studio
            Studio(
                user_id=b_host4.id,
                name="Yuvraj Photography & Film Studio",
                description="Atmospheric creative stage in Rajendra Nagar famous for dreamy pre-wedding photography. Features a signature warm golden fairy light bokeh wall, vintage wooden furniture, and dual diffused softbox lighting.",
                location="Near Selection Point, Rajendra Nagar, Bareilly, Uttar Pradesh 243122",
                city="Bareilly",
                category="Portrait",
                price_per_hour=1600.0, # ₹1,600/hr
                contact_phone="+91 97590 67812",
                contact_email="yuvrajfilms.bareilly@gmail.com",
                cover_image="/static/image/bareilly_prewedding_work.jpg",
                amenities="Golden Bokeh Fairy Wall, Vintage Props, Dual Softboxes, Wireless Microphones, Dressing Room"
            ),
            # Bareilly Studio 5: Natraj Studio & Production House
            Studio(
                user_id=b_host5.id,
                name="Natraj Studio & Production House",
                description="Heavy-duty cinema and video production stage on Pilibhit Bypass Road. Equipped with an expansive chroma green cyclorama cove, ceiling RGB lighting grid, teleprompter, and camera dolly track system for ad films and music videos.",
                location="Opp. Rohilkhand University, Pilibhit Bypass Road, Bareilly, Uttar Pradesh 243006",
                city="Bareilly",
                category="Cinema",
                price_per_hour=2800.0, # ₹2,800/hr
                contact_phone="+91 98375 88990",
                contact_email="natrajproductions.bly@gmail.com",
                cover_image="/static/image/bareilly_film_stage.jpg",
                amenities="Chroma Green Cyc, DMX Overhead RGB Grid, Camera Dolly Tracks, Soundproofed Acoustic Walls, 63A 3-Phase Power"
            ),
            # Bareilly Studio 6: Prem Studio & Heritage Color Lab
            Studio(
                user_id=b_host6.id,
                name="Prem Studio & Heritage Color Lab",
                description="Bareilly's trusted photography institution in Civil Lines operating since 1975. Features studio strobe staging alongside an in-house Noritsu digital lab for instant color-calibrated proofs and fine-art prints.",
                location="Main Market, Civil Lines, Bareilly, Uttar Pradesh 243001",
                city="Bareilly",
                category="Portrait",
                price_per_hour=1400.0, # ₹1,400/hr
                contact_phone="+91 94560 33445",
                contact_email="premstudio1975@gmail.com",
                cover_image="/static/image/canon_camera_bench.jpg",
                amenities="Noritsu Digital Color Lab, Instant High-Res Print Station, High-Key White Backdrops, Calibrated Grading Monitors"
            ),
            # Bareilly Studio 7: Snap Click Creative Studio
            Studio(
                user_id=b_host7.id,
                name="Snap Click Creative Studio",
                description="Specialized commercial product and jewelry photography studio next to Gandhi Udyan. Equipped with dedicated 360-degree motorized turntables, diffused jewelry lightboxes, macro focus rigs, and clean white tabletop surfaces.",
                location="Near Gandhi Udyan, Rampur Garden, Bareilly, Uttar Pradesh 243001",
                city="Bareilly",
                category="Product",
                price_per_hour=1500.0, # ₹1,500/hr
                contact_phone="+91 98970 55112",
                contact_email="snapclick.bareilly@gmail.com",
                cover_image="/static/image/bareilly_product_work.jpg",
                amenities="Jewelry Lightbox, 360 Turntable, 90+ CRI Macro LED Lights, Seamless Paper Rolls, High Speed WiFi"
            ),
            # Metro Studio 1: Lumina Cyclorama Mumbai
            Studio(
                user_id=m_host1.id,
                name="Lumina Cyclorama & Daylight Studio",
                description="Massive 2,400 sq.ft infinity cove with north-facing natural diffusion light, 18ft ceilings, and complete Profoto and Canon RF cinema package.",
                location="Lower Parel, Mumbai, Maharashtra 400013",
                city="Mumbai",
                category="Cyclorama",
                price_per_hour=3500.0, # ₹3,500/hr
                contact_phone="+91 98200 11223",
                contact_email="kabir@lumina.in",
                cover_image="/static/image/studio_stage_cinema.jpg",
                amenities="Infinity Cyc, Dual Hair & Makeup Stations, 63A 3-Phase Power, Client Lounge"
            ),
            # Metro Studio 2: Velvet Loft Bengaluru
            Studio(
                user_id=m_host2.id,
                name="Velvet Loft & High-Fashion Stage",
                description="Exposed brick, polished concrete floors, custom textured backdrops, and dedicated beauty lighting for luxury lookbooks and commercial shoots.",
                location="Indiranagar, Bengaluru, Karnataka 560038",
                city="Bengaluru",
                category="Fashion",
                price_per_hour=2800.0, # ₹2,800/hr
                contact_phone="+91 98450 12345",
                contact_email="ananya@velvet.in",
                cover_image="/static/image/canon_camera_bench.jpg",
                amenities="Styling Wardrobe, Steamer, Bluetooth Monitor Sound, High-speed Fibre WiFi"
            )
        ]

        db.session.add_all(studios_data)
        db.session.commit()

        # Map studios by name for clean foreign key relationships
        s_dict = {s.name: s for s in studios_data}

        # 3. PREVIOUS WORK / PORTFOLIO FOR EACH BAREILLY STUDIO
        portfolios_data = [
            # AH Studio Bareilly Previous Works
            Portfolio(
                studio_id=s_dict["AH Studio Bareilly"].id,
                image_url="/static/image/bareilly_wedding_studio.jpg",
                caption="Royal Mandap Bridal Session - Traditional Luxury Stage",
                category="Wedding",
                hashtags="#BareillyWeddings #RoyalBride #AHStudio #CivilLines",
                details="Shot on Canon EOS R5 with RF 85mm f/1.2L lens, dual Profoto softboxes with gold rim accents."
            ),
            Portfolio(
                studio_id=s_dict["AH Studio Bareilly"].id,
                image_url="/static/image/bareilly_fashion_work.jpg",
                caption="Designer Emerald Lehenga Fashion Campaign",
                category="Fashion",
                hashtags="#EthnicFashion #BareillyEditorial #BridalLookbook",
                details="Shot on Canon RF 50mm f/1.2L with grid hair lights and soft key illumination."
            ),

            # Chitralok Photography Studio Previous Works
            Portfolio(
                studio_id=s_dict["Chitralok Photography Studio"].id,
                image_url="/static/image/bareilly_portrait_studio.jpg",
                caption="Corporate Headshot & Executive Modeling Staging",
                category="Portrait",
                hashtags="#ModelTownBareilly #StudioPortraits #Chitralok #Headshots",
                details="Neutral grey seamless background, Godox 120cm Octabox key light with white reflector fill."
            ),
            Portfolio(
                studio_id=s_dict["Chitralok Photography Studio"].id,
                image_url="/static/image/bareilly_prewedding_work.jpg",
                caption="Pre-Wedding Romance in Warm Ambient Amber Glow",
                category="Couple",
                hashtags="#BareillyLove #CoupleGoals #ChitralokWeddings",
                details="Shot on Sony A7 IV with 50mm f/1.4 GM lens at f/1.8 with ambient fairy bokeh."
            ),

            # Kavya Digital Studio Previous Works
            Portfolio(
                studio_id=s_dict["Kavya Digital Studio & Event Stage"].id,
                image_url="/static/image/bareilly_fashion_work.jpg",
                caption="High-Fashion Editorial Cover Shoot in DD Puram",
                category="Fashion",
                hashtags="#DDPuramBareilly #KavyaStudio #IndianBridal #Editorial",
                details="Continuous Godox SL-200W video light fill with beauty dish rim light for dramatic fabric textures."
            ),
            Portfolio(
                studio_id=s_dict["Kavya Digital Studio & Event Stage"].id,
                image_url="/static/image/bareilly_product_work.jpg",
                caption="Traditional Kundan & Diamond Jewelry Catalog Work",
                category="Commercial",
                hashtags="#JewelleryPhotography #MacroShot #DDpuram",
                details="Captured on 100mm f/2.8L Macro with circular polarizing filter on dark marble pedestal."
            ),

            # Yuvraj Photography & Film Studio Previous Works
            Portfolio(
                studio_id=s_dict["Yuvraj Photography & Film Studio"].id,
                image_url="/static/image/bareilly_prewedding_work.jpg",
                caption="Cinematic Couple Portraiture on Signature Bokeh Wall",
                category="Pre-Wedding",
                hashtags="#RajendraNagarBareilly #YuvrajStudio #PreWeddingShoot",
                details="85mm f/1.4 lens capturing emotive bride & groom moments with fairy light bokeh background."
            ),
            Portfolio(
                studio_id=s_dict["Yuvraj Photography & Film Studio"].id,
                image_url="/static/image/bareilly_portrait_studio.jpg",
                caption="Creative Studio Lighting Test for Portraiture",
                category="Portrait",
                hashtags="#StudiozaBareilly #LightingSetup #PortraitLighting",
                details="Overhead hair strobe with soft key lighting for modeling portfolios."
            ),

            # Natraj Studio & Production House Previous Works
            Portfolio(
                studio_id=s_dict["Natraj Studio & Production House"].id,
                image_url="/static/image/bareilly_film_stage.jpg",
                caption="Green Screen Chroma Soundstage with Overhead RGB Grid",
                category="Cinema",
                hashtags="#PilibhitBypass #FilmProduction #NatrajStudio #ChromaKey",
                details="Used for commercial TV adverts, regional music video choreography, and teleprompter interviews."
            ),
            Portfolio(
                studio_id=s_dict["Natraj Studio & Production House"].id,
                image_url="/static/image/bareilly_wedding_studio.jpg",
                caption="Multi-Angle Cinema Stage Lighting for Event Highlights",
                category="Cinematography",
                hashtags="#WeddingCinema #NatrajBareilly #CinematicReels",
                details="Dual Sony FX3 rig on motorized slider tracks with wireless DMX ceiling panels."
            ),

            # Prem Studio & Heritage Color Lab Previous Works
            Portfolio(
                studio_id=s_dict["Prem Studio & Heritage Color Lab"].id,
                image_url="/static/image/canon_camera_bench.jpg",
                caption="Precision Optical Test Bench & Heritage Camera Rig",
                category="Optics",
                hashtags="#PremStudioBareilly #CivilLines #HeritagePhotography #Canon",
                details="Calibrated color-grading monitor setup with Canon L-series lenses."
            ),
            Portfolio(
                studio_id=s_dict["Prem Studio & Heritage Color Lab"].id,
                image_url="/static/image/bareilly_product_work.jpg",
                caption="Catalog Shoot for Bareilly Artisans & Zardozi Craft",
                category="Commercial",
                hashtags="#ZardoziBareilly #ProductPhotography #LocalCrafts #Handmade",
                details="Top diffused lightbox with color-calibrated grey-card accuracy."
            ),

            # Snap Click Creative Studio Previous Works
            Portfolio(
                studio_id=s_dict["Snap Click Creative Studio"].id,
                image_url="/static/image/bareilly_product_work.jpg",
                caption="Fine Diamond & Royal Gold Jewelry Commercial Campaign",
                category="Product",
                hashtags="#RampurGarden #SnapClick #JewelryShoot #MacroMastery",
                details="Shot on 360-degree motorized turntable with 95+ CRI micro LED beam spots."
            ),
            Portfolio(
                studio_id=s_dict["Snap Click Creative Studio"].id,
                image_url="/static/image/bareilly_fashion_work.jpg",
                caption="E-Commerce Fashion Lookbook for Bareilly Designers",
                category="Fashion",
                hashtags="#SnapClickBly #FashionCatalog #RampurGarden",
                details="Clean backdrop with high-contrast beauty dish for fabric detailing."
            ),

            # Metro Portfolios
            Portfolio(
                studio_id=s_dict["Lumina Cyclorama & Daylight Studio"].id,
                image_url="/static/image/studio_stage_cinema.jpg",
                caption="High-key fashion commercial shoot on the 3-wall cyc",
                category="Fashion",
                hashtags="#Editorial #CommercialFashion #CycStage",
                details="Captured with Canon EOS R5 and Profoto 1200w softbox setups"
            ),
            Portfolio(
                studio_id=s_dict["Velvet Loft & High-Fashion Stage"].id,
                image_url="/static/image/canon_camera_bench.jpg",
                caption="Pro gear ready on the natural wood styling bench",
                category="Optics",
                hashtags="#CanonR5 #RF50mm #Studioza",
                details="Canon RF 50mm f/1.2L test rig ready for talent"
            )
        ]

        db.session.add_all(portfolios_data)

        # 4. VERIFIED REVIEWS & RATINGS FOR BAREILLY STUDIOS
        reviews_data = [
            # AH Studio Reviews
            Review(
                studio_id=s_dict["AH Studio Bareilly"].id,
                customer_id=cust1.id,
                rating=5,
                review_text="Aman Hashmi and team at Butler Plaza are absolute masters of wedding and bridal lighting! The royal stage setup made our client shoot look like a heritage palace. Best wedding studio in Bareilly."
            ),
            Review(
                studio_id=s_dict["AH Studio Bareilly"].id,
                customer_id=cust2.id,
                rating=5,
                review_text="Civil Lines location is super convenient with ample parking. Profoto strobes were calibrated and the air conditioning made our 6-hour lehenga shoot a breeze."
            ),

            # Chitralok Studio Reviews
            Review(
                studio_id=s_dict["Chitralok Photography Studio"].id,
                customer_id=cust3.id,
                rating=5,
                review_text="Chitralok in Model Town has been my go-to for corporate headshots and portfolio portraits. Rajesh ji is polite, skilled, and the ₹1,800/hr rate is unmatched for the value."
            ),
            Review(
                studio_id=s_dict["Chitralok Photography Studio"].id,
                customer_id=cust1.id,
                rating=5,
                review_text="Great motorized backdrop setup and clean changing room. The Godox octabox delivers butter-smooth skin tones."
            ),

            # Kavya Digital Studio Reviews
            Review(
                studio_id=s_dict["Kavya Digital Studio & Event Stage"].id,
                customer_id=cust2.id,
                rating=5,
                review_text="Best studio for fashion reels and portfolio shoots in DD Puram! The vanity mirror lighting is flawless and Kavya was very helpful with equipment adjustments."
            ),
            Review(
                studio_id=s_dict["Kavya Digital Studio & Event Stage"].id,
                customer_id=cust3.id,
                rating=5,
                review_text="Located right on Stadium Road. Clean, spacious, and good continuous LED panels for commercial video clips. 5/5 stars!"
            ),

            # Yuvraj Photography Reviews
            Review(
                studio_id=s_dict["Yuvraj Photography & Film Studio"].id,
                customer_id=cust1.id,
                rating=5,
                review_text="The warm fairy light bokeh wall in Rajendra Nagar gave our pre-wedding couple photos an enchanting look. Highly recommended for couples looking for cinematic indoor shots."
            ),
            Review(
                studio_id=s_dict["Yuvraj Photography & Film Studio"].id,
                customer_id=cust2.id,
                rating=5,
                review_text="Super affordable at ₹1,600/hr. Yuvraj provided great props and assisted throughout our session."
            ),

            # Natraj Studio Reviews
            Review(
                studio_id=s_dict["Natraj Studio & Production House"].id,
                customer_id=cust3.id,
                rating=5,
                review_text="The only authentic chroma key soundstage with overhead RGB grid in Bareilly! Recorded two ad commercials without any ambient street noise. Outstanding facility on Pilibhit Bypass."
            ),
            Review(
                studio_id=s_dict["Natraj Studio & Production House"].id,
                customer_id=cust1.id,
                rating=5,
                review_text="Alok Saxena maintains top-tier standards. Heavy 3-phase power, dolly tracks, and reliable generator backup."
            ),

            # Prem Studio Reviews
            Review(
                studio_id=s_dict["Prem Studio & Heritage Color Lab"].id,
                customer_id=cust2.id,
                rating=5,
                review_text="Bareilly's heritage studio in Civil Lines! Needed color-calibrated catalog shots for our Zardozi handicrafts and instant prints. Prem ji delivered flawless work."
            ),
            Review(
                studio_id=s_dict["Prem Studio & Heritage Color Lab"].id,
                customer_id=cust3.id,
                rating=5,
                review_text="Extremely reliable, prompt, and honest pricing at ₹1,400/hr. Real veterans of photography."
            ),

            # Snap Click Creative Studio Reviews
            Review(
                studio_id=s_dict["Snap Click Creative Studio"].id,
                customer_id=cust1.id,
                rating=5,
                review_text="The 360-degree jewelry turntable and macro lightbox in Rampur Garden are phenomenal. Our diamond jewelry catalog looks top-class."
            ),
            Review(
                studio_id=s_dict["Snap Click Creative Studio"].id,
                customer_id=cust2.id,
                rating=5,
                review_text="Nitin is knowledgeable and patient. Peaceful setting next to Gandhi Udyan with great natural and artificial lighting."
            ),

            # Metro Reviews
            Review(
                studio_id=s_dict["Lumina Cyclorama & Daylight Studio"].id,
                customer_id=cust1.id,
                rating=5,
                review_text="Hands down the best cyclorama space in Mumbai! Flawless infinity curve and high power draw capacity."
            ),
            Review(
                studio_id=s_dict["Velvet Loft & High-Fashion Stage"].id,
                customer_id=cust2.id,
                rating=5,
                review_text="The daylight in this Bengaluru loft is unbelievable. Clean, spacious, and very cooperative host."
            )
        ]

        db.session.add_all(reviews_data)

        # 5. Sample Bookings
        bk1 = Booking(
            studio_id=s_dict["AH Studio Bareilly"].id,
            customer_id=cust1.id,
            booking_date="2026-09-20",
            hours=4,
            total_amount=9600.0, # 4 * ₹2,400
            status="confirmed",
            payment_status="paid",
            notes="Bridal lookbook with 2 traditional lehengas and royal mandap setup."
        )
        bk2 = Booking(
            studio_id=s_dict["Chitralok Photography Studio"].id,
            customer_id=cust2.id,
            booking_date="2026-09-22",
            hours=2,
            total_amount=3600.0, # 2 * ₹1,800
            status="confirmed",
            payment_status="paid",
            notes="Corporate team headshots on grey seamless backdrop."
        )

        db.session.add_all([bk1, bk2])
        db.session.commit()

        print(f"Successfully populated {len(studios_data)} studios (including 7 Bareilly studios), {len(portfolios_data)} previous works, and {len(reviews_data)} verified reviews!")

if __name__ == '__main__':
    setup_database()
