import pytest
from sqlbuilder.func.misc import GetLock, Inet6Aton, Inet6Ntoa, InetAton, InetNtoa, IsFreeLock, IsIpv4, IsIpv4Compat, IsIpv4Mapped, IsIpv6, IsUsedLock, MasterGtidWait, MasterPosWait, ReleaseAllLocks, ReleaseLock, Sleep, SysGuid, Uuid, UuidShort


def test_get_lock():
    get_lock_func = GetLock('lock_name', 10)
    assert str(get_lock_func) == "GET_LOCK(%s, %s)"
    assert get_lock_func.args == ['lock_name', 10]


def test_inet6_aton():
    inet6_aton_func = Inet6Aton('::1')
    assert str(inet6_aton_func) == "INET6_ATON(%s)"
    assert inet6_aton_func.args == ['::1']


def test_inet6_ntoa():
    inet6_ntoa_func = Inet6Ntoa('::1')
    assert str(inet6_ntoa_func) == "INET6_NTOA(%s)"
    assert inet6_ntoa_func.args == ['::1']


def test_inet_aton():
    inet_aton_func = InetAton('127.0.0.1')
    assert str(inet_aton_func) == "INET_ATON(%s)"
    assert inet_aton_func.args == ['127.0.0.1']


def test_inet_ntoa():
    inet_ntoa_func = InetNtoa(2130706433)
    assert str(inet_ntoa_func) == "INET_NTOA(%s)"
    assert inet_ntoa_func.args == [2130706433]


def test_is_free_lock():
    is_free_lock_func = IsFreeLock('lock_name')
    assert str(is_free_lock_func) == "IS_FREE_LOCK(%s)"
    assert is_free_lock_func.args == ['lock_name']


def test_is_ipv4():
    is_ipv4_func = IsIpv4('127.0.0.1')
    assert str(is_ipv4_func) == "IS_IPV4(%s)"
    assert is_ipv4_func.args == ['127.0.0.1']


def test_is_ipv4_compat():
    is_ipv4_compat_func = IsIpv4Compat('::1')
    assert str(is_ipv4_compat_func) == "IS_IPV4_COMPAT(%s)"
    assert is_ipv4_compat_func.args == ['::1']


def test_is_ipv4_mapped():
    is_ipv4_mapped_func = IsIpv4Mapped('::1')
    assert str(is_ipv4_mapped_func) == "IS_IPV4_MAPPED(%s)"
    assert is_ipv4_mapped_func.args == ['::1']


def test_is_ipv6():
    is_ipv6_func = IsIpv6('::1')
    assert str(is_ipv6_func) == "IS_IPV6(%s)"
    assert is_ipv6_func.args == ['::1']


def test_is_used_lock():
    is_used_lock_func = IsUsedLock('lock_name')
    assert str(is_used_lock_func) == "IS_USED_LOCK(%s)"
    assert is_used_lock_func.args == ['lock_name']


def test_master_gtid_wait():
    master_gtid_wait_func = MasterGtidWait('0-1-1', 10)
    assert str(master_gtid_wait_func) == "MASTER_GTID_WAIT(%s, %s)"
    assert master_gtid_wait_func.args == ['0-1-1', 10]

    master_gtid_wait_func = MasterGtidWait('0-1-1')
    assert str(master_gtid_wait_func) == "MASTER_GTID_WAIT(%s)"
    assert master_gtid_wait_func.args == ['0-1-1']


def test_master_pos_wait():
    master_pos_wait_func = MasterPosWait('mysql-bin.000001', 107, 10)
    assert str(master_pos_wait_func) == "MASTER_POS_WAIT(%s, %s, %s)"
    assert master_pos_wait_func.args == ['mysql-bin.000001', 107, 10]

    master_pos_wait_func = MasterPosWait('mysql-bin.000001', 107)
    assert str(master_pos_wait_func) == "MASTER_POS_WAIT(%s, %s)"
    assert master_pos_wait_func.args == ['mysql-bin.000001', 107]


def test_release_all_locks():
    release_all_locks_func = ReleaseAllLocks()
    assert str(release_all_locks_func) == "RELEASE_ALL_LOCKS()"
    assert release_all_locks_func.args == []


def test_release_lock():
    release_lock_func = ReleaseLock('lock_name')
    assert str(release_lock_func) == "RELEASE_LOCK(%s)"
    assert release_lock_func.args == ['lock_name']


def test_sleep():
    sleep_func = Sleep(10)
    assert str(sleep_func) == "SLEEP(%s)"
    assert sleep_func.args == [10]


def test_sys_guid():
    sys_guid_func = SysGuid()
    assert str(sys_guid_func) == "SYS_GUID()"
    assert sys_guid_func.args == []


def test_uuid():
    uuid_func = Uuid()
    assert str(uuid_func) == "UUID()"
    assert uuid_func.args == []


def test_uuid_short():
    uuid_short_func = UuidShort()
    assert str(uuid_short_func) == "UUID_SHORT()"
    assert uuid_short_func.args == []
