"""
Some elements of a chain require a LangChainVectorStore object with a running PG server to connect to locally.
This

**NOTE** If running tests on lxplus can just connect to CERN dbod and
update the TEST_DB_CONFIG to be correct for your server

Pytest fixtures to:
- Creates a test_db environment for testing the postgresql
- Creates fake twiki documents to write to the db with
- Populates the vectorstore with these documents
"""

import os
import tempfile
from pathlib import Path

import psycopg2
import pytest

from chATLAS_Embed import (
    PostgresParentChildVectorStore,
    RecursiveTextSplitter,
    syncedTwikiVectorStoreCreator,
)
from chATLAS_Embed.EmbeddingModels import SentenceTransformerEmbedding

# Database configuration for testing
TEST_DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "password",
    "database": "chatlas_test_db",
}


@pytest.fixture(scope="session")
def test_db():
    """Create a test database and clean it up after tests"""
    # Connect to default postgres database to create test database
    conn = psycopg2.connect(
        host=TEST_DB_CONFIG["host"],
        port=TEST_DB_CONFIG["port"],
        user=TEST_DB_CONFIG["user"],
        password=TEST_DB_CONFIG["password"],
        database="postgres",
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Drop test database if it exists and create new one
    cursor.execute(f"DROP DATABASE IF EXISTS {TEST_DB_CONFIG['database']}")
    cursor.execute(f"CREATE DATABASE {TEST_DB_CONFIG['database']}")

    cursor.close()
    conn.close()

    # Return connection string for the test database
    connection_string = f"postgresql://{TEST_DB_CONFIG['user']}:{TEST_DB_CONFIG['password']}@{TEST_DB_CONFIG['host']}:{TEST_DB_CONFIG['port']}/{TEST_DB_CONFIG['database']}"

    yield connection_string

    # Cleanup: Drop test database after all tests
    try:
        # Reconnect to the postgres database
        conn = psycopg2.connect(
            host=TEST_DB_CONFIG["host"],
            port=TEST_DB_CONFIG["port"],
            user=TEST_DB_CONFIG["user"],
            password=TEST_DB_CONFIG["password"],
            database="postgres",
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Disconnect any other sessions connected to the test database
        cursor.execute(f"""
            SELECT pg_terminate_backend(pid)
            FROM pg_stat_activity
            WHERE datname = '{TEST_DB_CONFIG["database"]}'
            AND pid <> pg_backend_pid();
        """)

        # Now drop the database
        cursor.execute(f"DROP DATABASE IF EXISTS {TEST_DB_CONFIG['database']}")
        cursor.close()
        conn.close()

    except psycopg2.errors.ObjectInUse:
        print(f"Database {TEST_DB_CONFIG['database']} is still in use, skipping drop.")


@pytest.fixture(scope="session")
def embedding_model():
    """Initialize the real embedding model"""
    return SentenceTransformerEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")


@pytest.fixture(scope="session")
def test_docs():
    """Create temporary test documents"""
    temp_dir = tempfile.mkdtemp()
    docs = []

    # Create sample TWiki documents
    test_contents = [
        {
            "filename": "ADCPlotOperations.txt",
            "content": """%META:TOPICINFO{author="BaseUserMapping_333" date="1416477899" format="1.1" version="1.369"}%
%META:TOPICPARENT{name="ADCOperationsDailyReports"}%
%STARTINCLUDE%
The ATLAS Experiment is one of the largest particle physics experiments at CERN.
It is designed to study particle collisions at the Large Hadron Collider.
The detector is 46 meters long and weighs about 7,000 tonnes.
ATLAS is one of two general-purpose detectors at the Large Hadron Collider (LHC). It investigates a wide range of physics,
from the Higgs boson to extra dimensions and particles that could make up dark matter.
Although it has the same scientific goals as the CMS experiment, it uses different technical solutions and a different magnet-system design.
Beams of particles from the LHC collide at the centre of the ATLAS detector making collision debris in the form of new particles,
which fly out from the collision point in all directions. Six different detecting subsystems arranged in layers around the collision point record the paths,
momentum, and energy of the particles, allowing them to be individually identified. A huge magnet system bends the paths of charged particles so that their momenta can be measured.

The interactions in the ATLAS detectors create an enormous flow of data. To digest the data, ATLAS uses an advanced
“trigger” system to tell the detector which events to record and which to ignore. Complex data-acquisition and
computing systems are then used to analyse the collision events recorded. At 46 m long, 25 m high and 25 m wide,
the 7000-tonne ATLAS detector is the largest volume particle detector ever constructed. It sits in a cavern 100 m
below ground near the main CERN site, close to the village of Meyrin in Switzerland.

below ground near the main CERN site, close to the village of Meyrin in Switzerland.
below ground near the main CERN site, close to the village of Meyrin in Switzerland.
below ground near the main CERN site, close to the village of Meyrin in Switzerland.
below ground near the main CERN site, close to the village of Meyrin in Switzerland.
below ground near the main CERN site, close to the village of Meyrin in Switzerland.

More than 5500 scientists from 245 institutes in 42 countries work on the ATLAS experiment (March 2022).
For the latest information, see here.
%STOPINCLUDE%
Extra other info which should not be included.
""",
        },
        {
            "filename": "Higgs_Boson.txt",
            "content": """%META:TOPICINFO{author="wikipedia" date="1736878918" format="1.1" version="1.3"}%
%META:TOPICPARENT{name="HiggsToTauTauToHH2012Winter"}%

%STARTINCLUDE%
TWiki https://twiki.cern.ch/twiki/bin/view/Main/WebHome
Atlas Web https://twiki.cern.ch/twiki/bin/view/Atlas/WebHome
AtlasUpgrade https://twiki.cern.ch/twiki/bin/view/Atlas/AtlasUpgrade
UpgradeProjectOffice https://twiki.cern.ch/twiki/bin/view/Atlas/UpgradeProjectOffice
UpgradeProjectOfficeCAD https://twiki.cern.ch/twiki/bin/view/Atlas/UpgradeProjectOfficeCAD
3DDataExchangeProcess https://twiki.cern.ch/twiki/bin/view/Atlas/3DDataExchangeProcess
-----HEADERS-----
h1: 3D Data exchange between ATLAS TC and collaboration institutes

-----TEXT-----
The Higgs boson was discovered by the ATLAS and CMS experiments in 2012.
This discovery confirmed the existence of the Higgs field, which gives particles their mass.
Peter Higgs and François Englert won the Nobel Prize in Physics for this theoretical prediction.
The Higgs boson, sometimes called the Higgs particle, is an elementary particle in the Standard Model of particle
physics produced by the quantum excitation of the Higgs field, one of the fields in particle physics theory.
In the Standard Model, the Higgs particle is a massive scalar boson with zero spin, even (positive) parity,
no electric charge, and no colour charge that couples to (interacts with) mass. It is also very unstable,
decaying into other particles almost immediately upon generation.
The Higgs field is a scalar field with two neutral and two electrically charged components that form a complex doublet
of the weak isospin SU(2) symmetry. Its "Sombrero potential" leads it to take a nonzero value everywhere
(including otherwise empty space), which breaks the weak isospin symmetry of the electroweak interaction and,
via the Higgs mechanism, gives a rest mass to all massive elementary particles of the Standard Model,
including the Higgs boson itself. The existence of the Higgs field became the last unverified part of the Standard
Model of particle physics, and for several decades was considered "the central problem in particle physics"
The Higgs boson, sometimes called the Higgs particle, is an elementary particle in the Standard Model of
particle physics produced by the quantum excitation of the Higgs field, one of the fields in particle physics theory.
As a layman I would now say… I think we have it.

“It” was the Higgs boson, the almost-mythical entity that had put particle physics in the global spotlight,
and the man proclaiming to be a mere layman was none other than CERN’s Director-General, Rolf Heuer.
Heuer spoke in the Laboratory’s main auditorium on 4 July 2012, moments after the CMS and ATLAS collaborations
at the Large Hadron Collider announced the discovery of a new elementary particle, which we now know is a Higgs boson.
Applause reverberated in Geneva from as far away as Melbourne, Australia, where delegates of the International
Conference on High Energy Physics were connected via video-conference.higgsjuly4,seminar,Milestones,
Higgs Boson Discovery,360
4 July 2012: A packed auditorium at CERN listens keenly to the announcement from CMS and ATLAS (Image: Maximilien Brice/CERN)
So what exactly is so special about this particle?“Easy! It is the first and only elementary scalar
particle we have observed,” grins Rebeca Gonzalez Suarez, who, as a doctoral student, was involved in
the CMS search for the Higgs boson. Easy for a physicist,
%STOPINCLUDE%
Extra text that should be ignored
            """,
        },
        {
            "filename": "LHC.txt",
            "content": """%META:TOPICINFO{author="google" date="1328618061" format="1.1" version="1.3"}%
%META:TOPICPARENT{name="LHC"}%

%STARTINCLUDE%
-----PARENT STRUCTURE----
TWiki https://twiki.cern.ch/twiki/bin/view/Main/WebHome
Atlas Web https://twiki.cern.ch/twiki/bin/view/Atlas/WebHome
AtlasUpgrade https://twiki.cern.ch/twiki/bin/view/Atlas/AtlasUpgrade
UpgradeProjectOffice https://twiki.cern.ch/twiki/bin/view/Atlas/UpgradeProjectOffice
UpgradeProjectOfficeCAD https://twiki.cern.ch/twiki/bin/view/Atlas/UpgradeProjectOfficeCAD
-----HEADERS-----
h1: 3D Data exchange between ATLAS TC and collaboration institutes

-----TEXT-----
The Large Hadron Collider (LHC) is the world's largest particle accelerator.
It consists of a 27-kilometer ring of superconducting magnets.
The LHC can collide protons at energies up to 13 TeV.
Inside the accelerator, two high-energy particle beams travel at close to the speed of light before they
are made to collide. The beams travel in opposite directions in separate beam pipes – two tubes kept at
ultrahigh vacuum. They are guided around the accelerator ring by a strong magnetic field maintained by
superconducting electromagnets. The electromagnets are built from coils of special electric cable that
operates in a superconducting state, efficiently conducting electricity without resistance or loss of energy.
This requires chilling the magnets to ‑271.3°C – a temperature colder than outer space. For this reason,
much of the accelerator is connected to a distribution system of liquid helium, which cools the magnets,
as well as to other supply services.

LHC stands for Large Hadron Collider, the world's largest and most powerful particle accelerator. It's located in a tunnel at CERN, the European Organization for Nuclear Research, on the Swiss-French border.
How it works
The LHC is a 27-kilometer ring of superconducting magnets that accelerate particles.
Beams of particles collide at four locations around the ring.
The collisions produce tiny fireballs that are hotter than the core of the sun.
What it's used for
The LHC has helped scientists discover the Higgs boson, a particle that gives mass to other particles.
The LHC may also help scientists understand why there is an imbalance of matter and antimatter in the universe.
Safety
The LHC Safety Assessment Group (LSAG) has concluded that the LHC collisions are not dangerous.
The LSAG's conclusions have been endorsed by CERN's Scientific Policy Committee.
History
The LHC was built between 1998 and 2008 with the help of over 10,000 scientists from hundreds of universities and laboratories.
It first started up on September 10, 2008.
%STOPINCLUDE%
       """,
        },
    ]

    for doc in test_contents:
        doc_path = Path(temp_dir) / doc["filename"]
        with open(doc_path, "w", encoding="UTF-8") as f:
            f.write(doc["content"])
        docs.append(doc_path)

    yield Path(temp_dir)

    # Cleanup temporary files
    for doc in docs:
        os.remove(doc)
    os.rmdir(temp_dir)


@pytest.fixture(scope="session")
def vector_store(test_db, embedding_model):
    """Initialize the vector store with test database"""
    return PostgresParentChildVectorStore(connection_string=test_db, embedding_model=embedding_model)


@pytest.fixture(scope="session")
def populated_vector_store(vector_store, test_docs):
    """Populate the vector store with test documents"""
    parent_splitter = RecursiveTextSplitter(chunk_size=2048, chunk_overlap=24)
    child_splitter = RecursiveTextSplitter(chunk_size=256, chunk_overlap=24)

    twiki_creator = syncedTwikiVectorStoreCreator(
        vector_store=vector_store,
        child_splitter=child_splitter,
        parent_splitter=parent_splitter,
        output_dir=Path("./test_output"),
    )

    twiki_creator.create_update_vectorstore(input_path=test_docs, update=True, verbose=True)

    yield vector_store

    del vector_store
