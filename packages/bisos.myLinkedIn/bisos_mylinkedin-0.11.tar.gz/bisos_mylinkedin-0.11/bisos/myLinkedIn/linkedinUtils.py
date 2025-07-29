import csv
import logging
from pathlib import Path
import zipfile
import vobject
from typing import Optional, List, Dict
from urllib.parse import urlparse


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class LinkedinId:
    """
    Utility functions for handling LinkedinId
    """

    @staticmethod
    def get_linkedin_idOBSOLETE(url: str) -> str:
        """
        Extract the LinkedIn ID from the profile URL.
        """
        return url.split('/')[-2]


    @staticmethod
    def fromUrl(url: str) -> str:
        """
        Extract the LinkedIn ID from the profile URL.
        """
        parts = url.rstrip('/').split('/')
        return parts[-1]

    @staticmethod
    def fromStr(vcard_dir: Path, uid: str) -> Optional[Path]:
        """
        Find the vCard file corresponding to the LinkedIn ID (UID) in the directory.
        """
        vcard_path = vcard_dir / f"{uid}.vcf"
        if vcard_path.exists():
            return vcard_path
        return None


    @staticmethod
    def fromPath(vcard_dir: Path, uid: str) -> Optional[Path]:
        """
        Find the vCard file corresponding to the LinkedIn ID (UID) in the directory.
        """
        vcard_path = vcard_dir / f"{uid}.vcf"
        if vcard_path.exists():
            return vcard_path
        return None


    @staticmethod
    def canonical(inStr: str) -> str:
        """
        Determine the canonical form of a LinkedIn identifier.

        This method checks the input string to determine if it is a URL, a file path,
        or a LinkedIn ID. It returns the LinkedIn ID in a canonical form based on the input type.

        - If the input is a URL, it extracts the LinkedIn ID using the fromUrl method.
        - If the input is a file path ending with '.vcf', it returns the file name without the extension.
        - If the input is a plain string, it assumes it is a LinkedIn ID and returns it as is.

        Args:
            inStr (str): The input string to be canonicalized.

        Returns:
            str: The canonical LinkedIn ID.
        """

        # Check if the input is a URL
        try:
            result = urlparse(inStr)
            if all([result.scheme, result.netloc]):
                return LinkedinId.fromUrl(inStr)
        except Exception:
            pass

        # Check if the input is a file path
        path = Path(inStr)
        if path.suffix == '.vcf':
            return path.stem

        # Otherwise, assume it's a LinkedIn ID
        return inStr

    @staticmethod
    def toUrl(id: str) -> str:
        """
        Convert linkedinId to linkedin Url.
        """
        return f"https://www.linkedin.com/in/{id}"



class VCard:
    """
    Utility functions for handling vCards and LinkedIn data files.
    """


    @staticmethod
    def read_csv(file_path: Path) -> List[Dict[str, str]]:
        """
        Read a CSV file and return the rows as a list of dictionaries.
        """
        if not file_path.exists():
            raise FileNotFoundError(f"{file_path} does not exist.")

        with file_path.open('r', encoding='utf-8') as f:
            return list(csv.DictReader(f))

    @staticmethod
    def write_vcard(vcard, vcard_path: Path) -> None:
        """
        Write the vCard object to a file.
        """
        with vcard_path.open('w', encoding='utf-8') as vcard_file:
            vcard_file.write(vcard.serialize())

    @staticmethod
    def read_vcard(vcard_path: Path):
        """
        Read a vCard from a file and return the vCard object.
        """
        with vcard_path.open('r', encoding='utf-8') as vcard_file:
            return vobject.readOne(vcard_file.read())

    @staticmethod
    def find_vcard(vcard_dir: Path, uid: str) -> Optional[Path]:
        """
        Find the vCard file corresponding to the LinkedIn ID (UID) in the directory.
        """
        vcard_path = vcard_dir / f"{uid}.vcf"
        if vcard_path.exists():
            return vcard_path
        return None

    @staticmethod
    def augment_vcard_with_contact_info(vcard_path: Path, contact_info: Dict[str, Optional[str]]) -> None:
        """
        Augments an existing vCard file with extracted LinkedIn contact info.
        """
        logger.info(f"Augmenting vCard at: {vcard_path}")

        if not vcard_path.exists():
            logger.error(f"vCard not found: {vcard_path}")
            return


        vcard_str = vcard_path.read_text(encoding="utf-8").strip()
        vcard = vobject.readOne(vcard_str)

        field_mapping = {
            "email": ("email", "INTERNET"),
            "phone": ("tel", "CELL"),
            "website": ("url", None),
            "twitter": ("x-twitter", None),
            "address": ("adr", None),
            "birthday": ("bday", None),
            "profile_url": ("x-linkedin", None),
        }

        for key, (field, type_param) in field_mapping.items():
            value = contact_info.get(key)
            if value:
                if hasattr(vcard, field):
                    vcard.contents[field][0].value = value
                else:
                    new_field = vcard.add(field)
                    new_field.value = value
                    if type_param:
                        new_field.type_param = type_param
                logger.debug(f"Updated {field} with: {value}")

        vcard_path.write_text(vcard.serialize(), encoding="utf-8")
        logger.info("vCard updated.")



    
class Common:

    @staticmethod
    def unzip_file(zip_path: Path, extract_to: Path) -> None:
        """Unzips a .zip file to the specified directory using pathlib.
        Use it like so: unzip_file(Path("LinkedInDataExport.zip"), Path("unzipped"))
        """
        logger.info(f"Unzipping {zip_path} to {extract_to}")
        extract_to.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
