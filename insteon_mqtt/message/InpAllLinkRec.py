#===========================================================================
#
# Input insteon all link record message.
#
#===========================================================================
from ..Address import Address
from .Base import Base
from .DbFlags import DbFlags


class InpAllLinkRec(Base):
    """All link database record.

    This is sent from the PLM modem to the host as a response to a
    record request and is the PLM modem all link database record that
    was requested.
    """
    msg_code = 0x57
    fixed_msg_size = 10

    #-----------------------------------------------------------------------
    @staticmethod
    def from_bytes(raw):
        """Read the message from a byte stream.

        This should only be called if raw[1] == msg_code and len(raw)
        >= msg_size().

        Args:
           raw   (bytes): The current byte stream to read from.

        Returns:
           Returns the constructed InpAllLinkRec object.
        """
        assert len(raw) >= InpAllLinkRec.fixed_msg_size
        assert raw[0] == 0x02 and raw[1] == InpAllLinkRec.msg_code

        flags = DbFlags.from_bytes(raw, 2)
        group = raw[3]
        addr = Address.from_bytes(raw, 4)
        data = raw[7:10]

        return InpAllLinkRec(flags, group, addr, data)

    #-----------------------------------------------------------------------
    def __init__(self, flags, group, addr, data):
        """Constructor

        Args:
          flags:  (DbFlags) The database record flags.
          group:  (int) The group the link is for.
          addr:   (Address) The address of the device in the link.
          data:   (bytes) 3 byte data record.
        """
        super().__init__()

        assert isinstance(flags, DbFlags)
        assert len(data) == 3

        self.flags = flags
        self.group = group
        self.addr = addr
        self.data = data
        self.on_level = data[0]
        self.ramp_rate = data[1]

    #-----------------------------------------------------------------------
    def __str__(self):
        return "InpAllLinkRec: %s grp: %s %s data: %#04x %#04x %#04x" % \
            (self.addr, self.group, self.flags, self.data[0], self.data[1],
             self.data[2])

    #-----------------------------------------------------------------------

#===========================================================================
